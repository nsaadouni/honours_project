#!/usr/bin/python

from PyKCS11 import *
from smartcard.System import readers

lib = '/usr/lib/x86_64-linux-gnu/pkcs11-spy.so'
pkcs11 = PyKCS11Lib()
pkcs11.load(lib)

slot = pkcs11.getSlotList()[-1]
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)

pin = '12345'
#session.login(pin)

reader = readers()[-1]
connection = reader.createConnection()
connection.connect()

print 'Simple program for sending apdu commands.'
print 'Use Ctrl-D (i.e. EOF) to exit'

try:
    while 1:
        _apdu = raw_input('apdu> ')
        if not _apdu: 
            continue
        elif _apdu == 'authenticate':
            #session.logout()
            #session.login(pin)
            continue
        try:
            connection.transmit([int(_, 16) for _ in _apdu.split()])
        except ValueError:
            print 'Invalid input'
            continue

except EOFError:
    pass

print ''
print 'Exit...'
