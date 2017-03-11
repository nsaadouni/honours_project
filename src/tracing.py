# Need to give credit to the virtual smarcard project!

import atexit
import signal
import sys
import struct
import socket

from smartcard.System import readers
import time
import hexdump as h

from PyKCS11 import *
import threading



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

                print ''
                print 'COMMAND'
                # print hexdump of message from API
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # convert api_ascii_msg -> intarray
                api_intarray_msg = asciistring_to_intarray(api_ascii_msg)
                # print api_intarray_msg

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

        # signal.signal(signal.SIGINT, stop)



# prints the trace with 'hexdump', but allows alterations for command and responses
def alter_trace(sock, connection):

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
                

            elif input_arg == '':

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                print sc_intarray_response  # print the message as an intarray for easy manipulation
                print '' # for space to the next command
                
                print 'Do you want the response? (y/N)'
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



##################################
# THESE STILL NEED TO BE CODED!! #
##################################

# This will alter the 8 byte card challenge to be increments of one and otehr
def alter_increment_login(sock, connection):
    
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

                print ''
                print 'COMMAND'
                # print hexdump of message from API
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # convert api_ascii_msg -> intarray
                api_intarray_msg = asciistring_to_intarray(api_ascii_msg)
                # print api_intarray_msg

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

        # signal.signal(signal.SIGINT, stop)


# This will alter all 8 byte card challenges to be '00 00 00 00 00 00 00 00'
def alter_login(sock, connection):

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

                print ''
                print 'COMMAND'
                # print hexdump of message from API
                h.hexdump(api_ascii_msg)
                print '' # to give space between command and resposne pair

                # convert api_ascii_msg -> intarray
                api_intarray_msg = asciistring_to_intarray(api_ascii_msg)
                # print api_intarray_msg

                # send the message from API to the smartcard
                data,sw1,sw2 = connection.transmit(api_intarray_msg)

                # generate sc_intarray_response
                sc_intarray_response = data + [sw1] + [sw2]

                # convert sc_intarray_response -> asciistring
                sc_ascii_response = intarray_to_asciistring(sc_intarray_response)

                print 'RESPONSE'
                # print response
                h.hexdump(sc_ascii_response)
                print '' # for space to the next command
                
                # send to API
                sendToVPICC(sock, sc_ascii_response)

        # signal.signal(signal.SIGINT, stop)



# This shall only be coded once I have the injection attack working!
def block_injection(sock, connection):
    return 0


###############################################################################################################################


###################################################################################
#                            Running Area                                         #
###################################################################################

arg = sys.argv[1]

if arg == 'print_traces':
    sock, connection = setup_socket_connection(2, 0)
    print_trace(sock, connection)

elif arg == 'alter_traces':
    sock, connection = setup_socket_connection(2, 0)
    alter_trace(sock, connection)

elif arg == 'alter_increment_login':
    sock, connection = setup_socket_connection(2, 0)
    alter_increment_login(sock, connection)

elif arg == 'alter_login':
    sock, connection = setup_socket_connection(2, 0)
    alter_login(sock, connection)

elif arg == 'halt_login':
    pass
    # This needs to be done for TOPT

elif arg == 'block_injection':
    pass


