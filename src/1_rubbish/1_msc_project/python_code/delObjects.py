
from PyKCS11 import *

#initialize cryptoki
# lib = '/usr/lib/x86_64-linux-gnu/pkcs11-spy.so'
lib = '/usr/lib/x64-athena/libASEP11.so'
pkcs11 = PyKCS11Lib()
pkcs11.load(lib)
print 'Initialization done.' 
# raw_input('Press Enter to continue...')

#open session
slot = pkcs11.getSlotList()[-1]
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
print 'Session opened. (No trace for this part)' 
# raw_input('Press Enter to continue...')

#login
pin = '0000000000000000'
session.login(pin)
print 'Login with pin 0000000000000000'
# raw_input('Press Enter to continue...')

#delete objects
objects = session.findObjects()
for o in objects:
    session.destroyObject(o)
print 'Objects deleted.'