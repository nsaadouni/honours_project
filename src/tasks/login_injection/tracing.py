import atexit
import signal
import sys
import struct
import socket
import time
from smartcard.System import readers
from PyKCS11 import *
from CryptoPlus.Cipher import DES3
import hashlib as hs
import binascii as ba
import hexdump as h



#-------------------------------------------------------#
#                   Global functions                    #
#-------------------------------------------------------#

_Csizeof_short = len(struct.pack('h', 0))

VPCD_CTRL_LEN = 1
VPCD_CTRL_OFF = 0
VPCD_CTRL_ON = 1
VPCD_CTRL_RESET = 2
VPCD_CTRL_ATR = 4

def sendToVPICC(sock, msg):

    sock.sendall(struct.pack('!H', len(msg)) + msg)

def recvFromVPICC(sock):
    sizestr = sock.recv(_Csizeof_short)
    if len(sizestr) == 0:
        raise socket.error
    size = struct.unpack('!H', sizestr)[0]

    if size:
        msg = sock.recv(size)
        if len(msg) == 0:
            raise socket.error
    else:
        msg = None

    return size, msg

def stop(_, __):
    connection.disconnect()
    sock.close()
    print ''
    print 'Exit...'
    sys.exit(0)

def asciistring_to_intarray(x):

    out = []
    for i in x:
        out.append(ord(i))
    return out

def intarray_to_asciistring(x):

    out = []
    for i in x:
        out.append(chr(i))
    return ''.join(out)

def hexstring_to_asciistring(x):
    out = []
    if len(x) % 2 != 0:
        x = '0' + x

    for i in range(0,len(x), 2):
        out.append(int((x[i]+x[i+1]),16))

    return intarray_to_asciistring(out)

def hexstring_to_intarray(x):
    out = []
    if len(x) % 2 != 0:
        x = '0' + x

    for i in range(0,len(x), 2):
        out.append(int((x[i]+x[i+1]),16))
        # ba.unhexlify(x[i]+x[i+1])
    return out
#-------------------------------------------------------#

def setup_socket_connection(reader_num, fake_reader):

    if fake_reader == 0:
        fake_reader_num = 35963
    elif fake_reader == 1:
        fake_reader_num = 35964


    # connect to the real card
    reader = readers()[reader_num]
    connection = reader.createConnection()
    connection.connect()

    # connect to vpicc
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', fake_reader_num))
    sock.settimeout(None)

    return sock, connection



###############################################################################################################################


# prints the trace with 'hexdump'
def print_trace(sock, connection):

    print 'Man in the middle tool started (for printing traces) ....'
    print ''

    counter = 0
    flag = 0

    while True:
        try:
            (size, api_ascii_msg) = recvFromVPICC(sock)
        except socket.error as e:
            sys.exit()

        if size == VPCD_CTRL_LEN:
            if api_ascii_msg == chr(VPCD_CTRL_OFF):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ON):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_RESET):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ATR):

                atr_hex_string = ('3B DC 18 FF 81 91 FE 1F C3 80 73 C8 21 13 66 01 0B 03 52 00 05 38')
                _atr_char_array = [chr(int(_, 16)) for _ in atr_hex_string.split()]
                atr = ''.join(_atr_char_array)
                # atr_ascii_string = hexstring_to_asciistring(atr_hex_string)
                sendToVPICC(sock, atr)
        
        else:
            
            # from virtual smartcard
            if size != len(api_ascii_msg):
                print format("Expected %u bytes, but received only %u",size, len(msg))


            test_array = asciistring_to_intarray(api_ascii_msg)
            if test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 1:
                
                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(test_array)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                # send to API
                sendToVPICC(sock, sc_ascii_response)
                continue

            elif test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 0:
                flag = 1


            input_arg = raw_input()
            if input_arg == '' or 'r':
                
                if input_arg == 'r':
                    counter = 0

                # print new command response pair counter
                counter += 1
                s = '----- APDU command/response pair ' + str(counter) + ' -----'
                print s

                # print ''
                # print 'COMMAND'
                # print hexdump of message from API
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # convert api_ascii_msg -> intarray
                api_intarray_msg = asciistring_to_intarray(api_ascii_msg)

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                # print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

        # signal.signal(signal.SIGINT, stop)



# prints the trace with 'hexdump', but allows alterations for command and responses
def alter_trace(sock, connection, print_int_array=False):

    print 'Man in the middle tool started (for printing traces) ....'
    print ''

    counter = 0
    flag = 0

    while True:
        try:
            (size, api_ascii_msg) = recvFromVPICC(sock)
        except socket.error as e:
            sys.exit()

        if size == VPCD_CTRL_LEN:
            if api_ascii_msg == chr(VPCD_CTRL_OFF):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ON):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_RESET):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ATR):

                atr_hex_string = ('3B DC 18 FF 81 91 FE 1F C3 80 73 C8 21 13 66 01 0B 03 52 00 05 38')
                _atr_char_array = [chr(int(_, 16)) for _ in atr_hex_string.split()]
                atr = ''.join(_atr_char_array)
                # atr_ascii_string = hexstring_to_asciistring(atr_hex_string)
                sendToVPICC(sock, atr)
        
        else:
            
            # from virtual smartcard
            if size != len(api_ascii_msg):
                print format("Expected %u bytes, but received only %u",size, len(msg))

            # prevents multiple ATR printing
            test_array = asciistring_to_intarray(api_ascii_msg)
            if test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 1:
                
                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(test_array)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                # send to API
                sendToVPICC(sock, sc_ascii_response)
                continue

            elif test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 0:
                flag = 1

            
            #---------------------------------------------------------------------------#
            counter += 1
            s = '----- APDU command/response pair ' + str(counter) + ' -----'
            print s

            print ''
            print 'COMMAND from API'
            # print hexdump of message from API
            h.hexdump(api_ascii_msg)

            # convert api_ascii_msg -> intarray
            api_intarray_msg = asciistring_to_intarray(api_ascii_msg)
            if print_int_array:
                print api_intarray_msg # print the message as an intarray for easy manipulation
            print '' # to give space between command and resposne pair

            #-----------------------------------------------------------------------------#
            print 'Do you want to to alter command? (y/N)'
            input_arg = raw_input()
            if input_arg == 'y':
                print 'Enter command (spaced integers)'
                input_arg = raw_input()
                api_intarray_msg = []
                for i in input_arg.split():
                    api_intarray_msg.append(int(i))
                
                # send changed command instead of the orginal command
                print 'command changed!'
                print ''

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                if print_int_array:
                    print sc_intarray_response  # print the message as an intarray for easy manipulation
                print '' # for space to the next command
                
                print 'Do you want to alter the response? (y/N)'
                input_arg = raw_input()
                if input_arg == 'y':
                    print "Enter response (spaced integers)"
                    input_arg = raw_input()
                    sc_intarray_response = []
                    for i in input_arg.split():
                        sc_intarray_response.append(int(i))
                    sc_ascii_response = intarray_to_asciistring(sc_intarray_response)
                    h.hexdump(sc_ascii_response)
                    print 'response changed!'
                    print ''

                # send to API
                sendToVPICC(sock, sc_ascii_response)
                

            elif input_arg == '' or input_arg == 'n':

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                if print_int_array:
                    print sc_intarray_response  # print the message as an intarray for easy manipulation
                print '' # for space to the next command
                
                print 'Do you want to alter the response? (y/N)'
                input_arg = raw_input()
                if input_arg == 'y':
                    print "Enter response (spaced integers)"
                    input_arg = raw_input()
                    sc_intarray_response = []
                    for i in input_arg.split():
                        sc_intarray_response.append(int(i))
                    sc_ascii_response = intarray_to_asciistring(sc_intarray_response)
                    h.hexdump(sc_ascii_response)
                    print 'response changed!'
                    print ''

                # send to API
                sendToVPICC(sock, sc_ascii_response)

        # signal.signal(signal.SIGINT, stop)



# DO THIS LAST!
# allows automated login response injection
# "if the first 8 bytes of the response if the session handle, we can now control it!"
def alter_inject_login_trace(sock, connection, print_int_array=False):

    print 'Man in the middle tool started (for printing traces) ....'
    print ''

    counter = 0
    flag = 0
    challenge = []
    response = []
    injection = 0

    while True:
        try:
            (size, api_ascii_msg) = recvFromVPICC(sock)
        except socket.error as e:
            sys.exit()

        if size == VPCD_CTRL_LEN:
            if api_ascii_msg == chr(VPCD_CTRL_OFF):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ON):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_RESET):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ATR):

                atr_hex_string = ('3B DC 18 FF 81 91 FE 1F C3 80 73 C8 21 13 66 01 0B 03 52 00 05 38')
                _atr_char_array = [chr(int(_, 16)) for _ in atr_hex_string.split()]
                atr = ''.join(_atr_char_array)
                # atr_ascii_string = hexstring_to_asciistring(atr_hex_string)
                sendToVPICC(sock, atr)
        
        else:
            
            # from virtual smartcard
            if size != len(api_ascii_msg):
                print format("Expected %u bytes, but received only %u",size, len(msg))

            # prevents multiple ATR printing
            test_array = asciistring_to_intarray(api_ascii_msg)
            if test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 1:
                
                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(test_array)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                # send to API
                sendToVPICC(sock, sc_ascii_response)
                continue

            elif test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 0:
                flag = 1

            
            #---------------------------------------------------------------------------#
            counter += 1
            s = '----- APDU command/response pair ' + str(counter) + ' -----'
            print s

            print ''
            print 'COMMAND from API'
            # print hexdump of message from API
            h.hexdump(api_ascii_msg)

            # convert api_ascii_msg -> intarray
            api_intarray_msg = asciistring_to_intarray(api_ascii_msg)
            if print_int_array:
                print api_intarray_msg # print the message as an intarray for easy manipulation
            print '' # to give space between command and resposne pair

            #-----------------------------------------------------------------------------#

            # HERE is where I should inject my own login script
            if api_intarray_msg[0:5] == [0, 132, 0, 0, 8]:
                print 'Do you want to automate the injection your own login response? (Y/n)'
                input_arg = raw_input()
                if input_arg == '' or input_arg == 'y':
                    injection = 1

                    # send the message from API to the smartcard
                    data,sw1,sw2 = connection.transmit(api_intarray_msg)

                    # generate sc_intarray_response
                    sc_intarray_response = data + [sw1] + [sw2]

                    #-------------------------------------------------------#
                    # calculate a valid response with a given challenge & save it
                    challenge = []
                    for i in data:
                        challenge.append(i)

                    response = []
                    response = login_response(challenge)
                    #-------------------------------------------------------#

                    # convert sc_intarray_response -> asciistring
                    sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                    print 'RESPONSE'
                    # print response
                    h.hexdump(sc_ascii_response)
                    if print_int_array:
                        print sc_intarray_response  # print the message as an intarray for easy manipulation
                    print '' # for space to the next command

                    # send to API
                    sendToVPICC(sock, sc_ascii_response)
                    continue

            elif api_intarray_msg[0:5] == [128, 32, 0, 0, 16] and injection == 1:
                    
                    # inject the respose (pinrt old and injected?)
                    injection = 0

                    print 'COMMAND injected'
                    
                    api_intarray_msg = response
                    response = []
                    api_ascii_msg = intarray_to_asciistring(api_intarray_msg)

                    # print hexdump of message from API
                    h.hexdump(api_ascii_msg)
                    if print_int_array:
                        print api_intarray_msg # print the message as an intarray for easy manipulation
                    print '' # to give space between command and resposne pair

                    # send the message from API to the smartcard
                    data,sw1,sw2 = connection.transmit(api_intarray_msg)

                    # generate sc_intarray_response
                    sc_intarray_response = data + [sw1] + [sw2]

                    # convert sc_intarray_response -> asciistring
                    sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                    print 'RESPONSE'
                    # print response
                    h.hexdump(sc_ascii_response)
                    if print_int_array:
                        print sc_intarray_response  # print the message as an intarray for easy manipulation
                    print '' # for space to the next command

                    # send to API
                    sendToVPICC(sock, sc_ascii_response)

                    continue
            else:
                    pass




            #-----------------------------------------------------------------------------#
            print 'Do you want to to alter command? (y/N)'
            input_arg = raw_input()
            if input_arg == 'y':
                print 'Enter command (spaced integers)'
                input_arg = raw_input()
                api_intarray_msg = []
                for i in input_arg.split():
                    api_intarray_msg.append(int(i))
                
                # send changed command instead of the orginal command
                print 'command changed!'
                print ''

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                if print_int_array:
                    print sc_intarray_response  # print the message as an intarray for easy manipulation
                print '' # for space to the next command
                
                print 'Do you want to alter the response? (y/N)'
                input_arg = raw_input()
                if input_arg == 'y':
                    print "Enter response (spaced integers)"
                    input_arg = raw_input()
                    sc_intarray_response = []
                    for i in input_arg.split():
                        sc_intarray_response.append(int(i))
                    sc_ascii_response = intarray_to_asciistring(sc_intarray_response)
                    h.hexdump(sc_ascii_response)
                    print 'response changed!'
                    print ''

                # send to API
                sendToVPICC(sock, sc_ascii_response)
                

            elif input_arg == '' or input_arg == 'n':

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                if print_int_array:
                    print sc_intarray_response  # print the message as an intarray for easy manipulation
                print '' # for space to the next command
                
                print 'Do you want to alter the response? (y/N)'
                input_arg = raw_input()
                if input_arg == 'y':
                    print "Enter response (spaced integers)"
                    input_arg = raw_input()
                    sc_intarray_response = []
                    for i in input_arg.split():
                        sc_intarray_response.append(int(i))
                    sc_ascii_response = intarray_to_asciistring(sc_intarray_response)
                    h.hexdump(sc_ascii_response)
                    print 'response changed!'
                    print ''

                # send to API
                sendToVPICC(sock, sc_ascii_response)

        # signal.signal(signal.SIGINT, stop)



###############################################################################################################################


def same_challenge_trace(sock, connection):
    print 'Man in the middle tool started (for printing traces) ....'
    print ''

    flag = 0
    counter = 0
    command_counter = 0

    while True:
        try:
            (size, api_ascii_msg) = recvFromVPICC(sock)
        except socket.error as e:
            sys.exit()

        if size == VPCD_CTRL_LEN:
            if api_ascii_msg == chr(VPCD_CTRL_OFF):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ON):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_RESET):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ATR):

                atr_hex_string = ('3B DC 18 FF 81 91 FE 1F C3 80 73 C8 21 13 66 01 0B 03 52 00 05 38')
                _atr_char_array = [chr(int(_, 16)) for _ in atr_hex_string.split()]
                atr = ''.join(_atr_char_array)
                # atr_ascii_string = hexstring_to_asciistring(atr_hex_string)
                sendToVPICC(sock, atr)
        
        else:
            
            # from virtual smartcard
            if size != len(api_ascii_msg):
                print format("Expected %u bytes, but received only %u",size, len(msg))


            test_array = asciistring_to_intarray(api_ascii_msg)
            if test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 1:
                
                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(test_array)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                # send to API
                sendToVPICC(sock, sc_ascii_response)
                continue

            elif test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 0:
                flag = 1

            #---------------------------------------------------------------------------#

            # convert api_ascii_msg -> intarray
            api_intarray_msg = asciistring_to_intarray(api_ascii_msg)

            # find and print get challenge command
            if api_intarray_msg[0:5] == [0, 132, 0, 0, 8]:

                # print new command response pair counter
                command_counter += 1
                s = '----- APDU command/response pair ' + str(counter) + ' -----'
                print s
                
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # alter the response here -> set the challenge
                if counter == 0:
                    sc_intarray_response = [0,0,0,0,0,0,0,0,144,0]
                    counter+=1

                elif counter == 1:
                    sc_intarray_response = [0,0,0,0,0,0,0,0,144,0]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

            # find and print verify command
            elif api_intarray_msg[0:5] == [128, 32, 0, 0, 16]:
                
                # print new command response pair counter
                command_counter += 1
                s = '----- APDU command/response pair ' + str(counter) + ' -----'
                print s
                
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

            # do not print anything else
            else:
                # send messages but do not print
                command_counter+=1

                # convert api_ascii_msg -> intarray
                api_intarray_msg = asciistring_to_intarray(api_ascii_msg)


                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)





        signal.signal(signal.SIGINT, stop)


def different_challenge_trace(sock, connection):
    print 'Man in the middle tool started (for printing traces) ....'
    print ''

    flag = 0
    counter = 0
    command_counter = 0

    while True:
        try:
            (size, api_ascii_msg) = recvFromVPICC(sock)
        except socket.error as e:
            sys.exit()

        if size == VPCD_CTRL_LEN:
            if api_ascii_msg == chr(VPCD_CTRL_OFF):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ON):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_RESET):
                pass
            elif api_ascii_msg == chr(VPCD_CTRL_ATR):

                atr_hex_string = ('3B DC 18 FF 81 91 FE 1F C3 80 73 C8 21 13 66 01 0B 03 52 00 05 38')
                _atr_char_array = [chr(int(_, 16)) for _ in atr_hex_string.split()]
                atr = ''.join(_atr_char_array)
                # atr_ascii_string = hexstring_to_asciistring(atr_hex_string)
                sendToVPICC(sock, atr)
        
        else:
            
            # from virtual smartcard
            if size != len(api_ascii_msg):
                print format("Expected %u bytes, but received only %u",size, len(msg))


            test_array = asciistring_to_intarray(api_ascii_msg)
            if test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 1:
                
                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(test_array)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                # send to API
                sendToVPICC(sock, sc_ascii_response)
                continue

            elif test_array == [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0] and flag == 0:
                flag = 1

            #---------------------------------------------------------------------------#

            # convert api_ascii_msg -> intarray
            api_intarray_msg = asciistring_to_intarray(api_ascii_msg)

            # find and print get challenge command
            if api_intarray_msg[0:5] == [0, 132, 0, 0, 8]:

                # print new command response pair counter
                command_counter += 1
                s = '----- APDU command/response pair ' + str(counter) + ' -----'
                print s
                
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # alter the response here -> set the challenge
                if counter == 0:
                    sc_intarray_response = [0,0,0,0,0,0,0,0,144,0]
                    counter+=1

                elif counter == 1:
                    sc_intarray_response = [0,0,0,0,0,0,0,1,144,0]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

            # find and print verify command
            elif api_intarray_msg[0:5] == [128, 32, 0, 0, 16]:
                
                # print new command response pair counter
                command_counter += 1
                s = '----- APDU command/response pair ' + str(counter) + ' -----'
                print s
                
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

            # do not print anything else
            else:
                # send messages but do not print
                command_counter+=1

                # convert api_ascii_msg -> intarray
                api_intarray_msg = asciistring_to_intarray(api_ascii_msg)


                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)



        signal.signal(signal.SIGINT, stop)



###############################################################################################################################

# This shall only be coded once I have the injection attack working!
def block_injection(sock, connection):
    

    return 0


###############################################################################################################################

# needs to return list of integers for the 16 byte response
# Na -> determined by the user (think this is the sesion handle)
# Nc -> card challenge, will be give as a list of integers (string)
#Na=[5, 65, 80, 153, 3, 155, 183, 162]
# This takes in the card challenge as a list of integers as a STRING
def login_response_input_integers(pin, card_challenege, Na=[0,0,0,0,0,0,0,0] ):

    # first process card challenge
    Nc = []
    for i in card_challenege.split():
        Nc.append(int(i))

    # create the password that is needed
    hash_sha1 = hs.new('sha1')
    hash_sha1.update(pin)
    password = hash_sha1.digest()[0:16]

    # create the message to encrypt
    msg = []
    for i in Na+Nc:
        msg.append(chr(i))
    msg = ''.join(msg)

    # encrypt message
    cipher = DES3.new(password, DES3.MODE_CBC, IV='\x00\x00\x00\x00\x00\x00\x00\x00')
    byte_resposne = cipher.encrypt(msg)
    hex_response = ba.hexlify(byte_resposne)

    response = []
    for i in hexstring_to_intarray(hex_response):
        response.append(i)

    return response


def resposne_print(response):
    

    msg = str(response)
    for i in msg.split('[')[1].split(']')[0].split(','):
        sys.stdout.write(i.strip() +' ')
    print ''





def login_response(Nc, Na=[0,0,0,0,0,0,0,0], pin='0000000000000000'):

    # create the password that is needed
    hash_sha1 = hs.new('sha1')
    hash_sha1.update(pin)
    password = hash_sha1.digest()[0:16]

    # create the message to encrypt
    msg = []
    for i in Na+Nc:
        msg.append(chr(i))
    msg = ''.join(msg)

    # encrypt message
    cipher = DES3.new(password, DES3.MODE_CBC, IV='\x00\x00\x00\x00\x00\x00\x00\x00')
    byte_resposne = cipher.encrypt(msg)
    hex_response = ba.hexlify(byte_resposne)

    response = [128, 32, 0, 0, 16]
    for i in hexstring_to_intarray(hex_response):
        response.append(i)

    return response




# can be used as a direct chanage in the alter trace!!
# DO NOT NEED -> INT ARRAY IS SENT TO CARD!

# DELETE ONCE I HAVE THE OTHER Fuction working
def login_response_ascii(pin, card_challenege, Na=[0,0,0,0,0,0,0,0]):

    # first process card challenge
    Nc = []
    for i in card_challenege.split():
        Nc.append(int(i))

    # create the password that is needed
    hash_sha1 = hb.new('sha1')
    hash_sha1.update(pin)
    password = hash_sha1.digest()[0:16]

    # create the message to encrypt
    msg = []
    for i in Na+Nc:
        msg.append(chr(i))
    msg = ''.join(msg)

    # encrypt message
    cipher = DES3.new(password, DES3.MODE_CBC, IV='\x00\x00\x00\x00\x00\x00\x00\x00')
    byte_resposne = cipher.encrypt(msg)
    hex_response = ba.hexlify(byte_resposne)

    # base of response -> add the inital 5 bytes!
    response = []
    for i in hexstring_to_intarray(hex_response):
        response.append(i)
    response_ascii = intarray_to_asciistring(response)

    return response_ascii



###############################################################################################################################


###################################################################################
#                            Running Area                                         #
###################################################################################

arg = sys.argv[1]

if arg == 'print_trace':
    # prints a trace of the APDU communication
    sock, connection = setup_socket_connection(2, 0)
    print_trace(sock, connection)

elif arg == 'alter_trace':
    # allows you to alter the communication of the APUD communication
    sock, connection = setup_socket_connection(2, 0)
    alter_trace(sock, connection)

elif arg == 'alter_inject_response_trace':
    # allows you to alter the communication of the APUD communication
    sock, connection = setup_socket_connection(2, 0)
    alter_inject_login_trace(sock, connection)

#########################################################
elif arg == 'same_challenge':
    sock, connection = setup_socket_connection(2, 0)
    same_challenge_trace(sock, connection)

elif arg == 'different_challenge':
    sock, connection = setup_socket_connection(2, 0)
    different_challenge_trace(sock, connection)
#########################################################

elif arg == 'halt_login':
    # This will halt the communication stream when the response for the
    # login protocol is about to be sent from API -> Card
    pass

elif arg == 'block_injection':
    # If I can reverse engineer the Secure Messaging protocol
    # This script will automate injecting my own key and grabbing the block cipher key thats in transit
    pass

#########################################################
# This produces a valid response given the correct pin, and challenge.
elif arg == 'login_response':
    challenge = sys.argv[2]
    response = login_response_input_integers('0000000000000000', challenge)
    # print response
    resposne_print(response)
#########################################################