#!/usr/bin/python

# A small part of this code is taken from https://github.com/frankmorgner/vsmartcard/blob/master/virtualsmartcard/src/vpicc/virtualsmartcard/VirtualSmartcard.py
# The remaining, which is a larger part, is original. 

import atexit
import signal
import sys
import struct
import socket
from smartcard.System import readers

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

    if size:
        msg = sock.recv(size)
        if len(msg) == 0:
            raise socket.error
    else:
        msg = None

    return size, msg

def char_to_hex(char):
    return hex(ord(char)).replace('x', '0')[-2:]

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
        _apdu_hex_array = [char_to_hex(_) for _ in msg]
        apdu = ' '.join(_apdu_hex_array)
        print '\033[94m' + 'toCard: ' + apdu + '\033[0m'

        _is_relaying_message = False

        while True:
            if _is_relaying_message:
                action = 'toApp'
                _message_hex_str = response
                _is_relaying_message = False
          
            else:
                try:
                    _input = raw_input('\033[2m' + '> ' + '\033[0m').strip()
                    if not _input:
                        raise ValueError
                    try:
                        action, _message_hex_str = _input.split(' ', 1)
                    except ValueError:
                        action = _input
                        if action == 'r':
                            #print '\033[2m\033[95m' + 'relaying apdu/response pair...' + '\033[0m'
                            _is_relaying_message = True
                            action = 'toCard'
                            _message_hex_str = apdu
                        elif action in ['toCard', 'toApp']:
                            print '\033[91m' + 'no input message...' + '\033[0m'
                            raise ValueError
                except ValueError:
                    continue

            if action == 'toCard':
                #print '\033[2m\033[94m' + 'sent apdu: ' + _message_hex_str + '\033[0m'
                message = [int(_, 16) for _ in _message_hex_str.split()]
                (data, sw1, sw2) = connection.transmit(message)
                _response_int_array = data + [sw1] + [sw2]
                _response_hex_array = []
                for _ in _response_int_array:
                    _response_hex_array.append(char_to_hex(chr(_)))
                response = ' '.join(_response_hex_array)
                print '\033[92m' + 'toApp: ' + response + '\033[0m'

            elif action == 'toApp':
                #print '\033[2m\033[92m' + 'sent response: ' + _message_hex_str + '\033[0m'
                _message_hex_array = _message_hex_str.split()
                _message_chr_array = []
                for _ in _message_hex_array:
                    _message_chr_array.append(chr(int(_, 16)))
                message = ''.join(_message_chr_array)
                sendToVPICC(message)
                break

            else:
                print '\033[91m' + 'invalid operation...' + '\033[0m'

    signal.signal(signal.SIGINT, stop)
