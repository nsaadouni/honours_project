#!/usr/bin/python

from PyKCS11 import *

# 	/usr/lib/pkcs11/pkcs11-spy.so

lib = "/usr/lib/x64-athena/libASEP11.so"
lib2= "/usr/lib/pkcs11/pkcs11-spy.so"
pkcs11 = PyKCS11Lib()	
pkcs11.load(lib)

slot = pkcs11.getSlotList()[2]
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)

pin = '123456'
session.login(pin)


#print pkcs11.getInfo()
#print pkcs11.getTokenInfo(slot)

#for key in CKF:
 #   print str(key) + "," +str(CKF[key])
#print "is login required? " + str(CKF_LOGIN_REQUIRED)
#print CKF_RNG, CKF_LOGIN_REQUIRED, CKF_TOKEN_INITIALIZED, CKF_USER_PIN_INITIALIZED
#print session.getSessionInfo()



# CKU_USER -> standard user
# admin account login with pin, 0

# print CKU
# try:
#     session.login(pin, 0)
# except PyKCS11Error as e:
#     print e

#print hex(CKR_PIN_INCORRECT)

#session.logout()
#session.closeSession()
