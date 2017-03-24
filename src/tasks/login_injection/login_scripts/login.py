#!/usr/bin/python

from PyKCS11 import *
import time
import sys

# 	/usr/lib/pkcs11/pkcs11-spy.so

arg = int(sys.argv[1])
# lib = "/usr/lib/pkcs11/pkcs11-spy.so"
lib = "/usr/lib/x64-athena/libASEP11.so"
pkcs11 = PyKCS11Lib()
pkcs11.load(lib)

pin = '0000000000000000'


try:
	slot = pkcs11.getSlotList()[arg]
	session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
	session.login(pin)
except PyKCS11Error as e:
	print e
	pass


