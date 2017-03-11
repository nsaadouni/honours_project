#!/usr/bin/python

from PyKCS11 import *
import time

# 	/usr/lib/pkcs11/pkcs11-spy.so

lib = "/usr/lib/x64-athena/libASEP11.so"
lib2= "/usr/lib/pkcs11/pkcs11-spy.so"
pkcs11 = PyKCS11Lib()	
pkcs11.load(lib)

slot = pkcs11.getSlotList()[0]
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)

pin = '0000000000000000'

# print 'quick sleep to allow everthing to run smoothly'
# time.sleep(5)

try:
    session.login(pin)
except PyKCS11Error as e:
    print e

pin = '1111111111111111'

try:
    session.login(pin)
except PyKCS11Error as e:
    print e

# try:
#     session.login(pin)
# except PyKCS11Error as e:
#     print e

# try:
#     session.login(pin)
# except PyKCS11Error as e:
#     print e

# try:
#     session.login(pin)
# except PyKCS11Error as e:
#     print e

# # pin = '0000000000000001'

# try:
#     session.login(pin)
#     session.logout()
# except PyKCS11Error as e:
#     print e

# # pin = '0000000000000002'

# try:
#     session.login(pin)
# except PyKCS11Error as e:
#     print e

# # pin = '0000000000000003'

# try:
#     session.login(pin)
#     session.logout()
# except PyKCS11Error as e:
#     print e

# try:
#     session.login(pin)
# except PyKCS11Error as e:
#     print e

# try:
#     session.login(pin)
#     session.logout()
# except PyKCS11Error as e:
#     print e

# try:
#     session.login(pin)
# except PyKCS11Error as e:
#     print e

# try:
#     session.login(pin)
#     session.logout()
# except PyKCS11Error as e:
#     print e

#print pkcs11.getInfo()
#print '-------------------------'
#print pkcs11.getTokenInfo(slot)
#print '-------------------------'
#print pkcs11.getSlotInfo(slot)
#print '-------------------------'

#for key in CKF:
#    print str(key) + "," +str(CKF[key])
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
