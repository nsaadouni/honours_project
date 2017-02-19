from PyKCS11 import *
import sys
import time


"""
List of functions that I have to have traces for!!

session.login()
session.findObjects()
session.generateKeyPair()
session.createObject()
session.destroyObject()
session.encrypt()
session.decrypt()
session.sign()
session.verify()
session.__setattr__()
session.wrapKey()
session.unwrapKey()
"""


"""
12 -> 15 functions
1.  login
2.  findObjects
3.  generateKeyPair (RSA)
4. createObject (AES, DES, DES2, DES3) [4, 5, 6, 7]
8.  destroyObject
9.  encrypt
10. decrypt
11. sign
12. verify
13. setAttribute
14. wrapKey (don't think this works!)
15. unwrapKey
"""


# arg = int(sys.argv[1])
# lib = "/usr/lib/pkcs11/pkcs11-spy.so"
lib = "/usr/lib/x64-athena/libASEP11.so"
pkcs11 = PyKCS11Lib()
pkcs11.load(lib)

pin = '0000000000000000'


def generateKeyPair_rsa():
    return 0

def generate_AES(id, label):
    template = (
        (LowLevel.CKA_CLASS, LowLevel.CKO_SECRET_KEY),
        (LowLevel.CKA_KEY_TYPE, LowLevel.CKK_AES),
        (LowLevel.CKA_VALUE_LEN, 32),
        (LowLevel.CKA_LABEL, label),
        (LowLevel.CKA_ID, chr(id)),
        (LowLevel.CKA_PRIVATE, True),
        (LowLevel.CKA_SENSITIVE, True),
        (LowLevel.CKA_ENCRYPT, True),
        (LowLevel.CKA_DECRYPT, True),
        (LowLevel.CKA_SIGN, True),
        (LowLevel.CKA_VERIFY, True),
        (LowLevel.CKA_TOKEN, True),
        (LowLevel.CKA_WRAP, True),
        (LowLevel.CKA_UNWRAP, True),
        (LowLevel.CKA_EXTRACTABLE, False))
    t = session._template2ckattrlist(template)
    m = LowLevel.CK_MECHANISM()
    m.mechanism = LowLevel.CKM_AES_KEY_GEN
    key = LowLevel.CK_OBJECT_HANDLE()
    rv = pkcs11.lib.C_GenerateKey(session.session, m, t, key)
    if rv != LowLevel.CKR_OK:
        raise PyKCS11Error(rv)


def generate_DES(id, label):
    template = (
        (LowLevel.CKA_CLASS, LowLevel.CKO_SECRET_KEY),
        (LowLevel.CKA_KEY_TYPE, LowLevel.CKK_DES),
        (LowLevel.CKA_LABEL, label),
        (LowLevel.CKA_ID, chr(id)),
        (LowLevel.CKA_PRIVATE, True),
        (LowLevel.CKA_SENSITIVE, True),
        (LowLevel.CKA_ENCRYPT, True),
        (LowLevel.CKA_DECRYPT, True),
        (LowLevel.CKA_SIGN, True),
        (LowLevel.CKA_VERIFY, True),
        (LowLevel.CKA_TOKEN, True),
        (LowLevel.CKA_WRAP, True),
        (LowLevel.CKA_UNWRAP, True),
        (LowLevel.CKA_EXTRACTABLE, False))
    t = session._template2ckattrlist(template)
    m = LowLevel.CK_MECHANISM()
    m.mechanism = LowLevel.CKM_DES_KEY_GEN
    key = LowLevel.CK_OBJECT_HANDLE()
    rv = pkcs11.lib.C_GenerateKey(session.session, m, t, key)
    if rv != LowLevel.CKR_OK:
        raise PyKCS11Error(rv)

def generate_DES2(id, label):
    return 0

def generate_DES3(id, label):
    return 0

def encrypt():
    return 0

def decrypt():
    return 0

def verify():
    return 0

def sign():
    return 0

def setAttributes():
    return 0

def wrapKey():
    return 0

def unwrapKey():
    return 0

#--------------------------------------------------------#

def login():
    try:
        slot = pkcs11.getSlotList()[2]
        session = pkcs11.openSession(slot, LowLevel.CKF_SERIAL_SESSION | LowLevel.CKF_RW_SESSION)
        session.login(pin)
    except PyKCS11Error as e:
        print e

    return session

def destroyObjects(session, objects):
    for o in objects:
        session.destroyObject(o)

def findObjects(session):
    objects = session.findObjects()
    return objects


session = login()
# print 'login completed'
# print ''
# i = raw_input()
# generate_AES(1, "testing")


pkcs11_objects = findObjects(session)
print pkcs11_objects

# i = raw_input()
# destroyObjects(session, pkcs11_objects)











# if __name__ == '__main__':
#
#     functions = [login]
#     function_names = ['login']
#
#     counter = 0
#     for i in function_names:
#         if sys.argv[2] == i:
#             functions[counter]()
#             break
#         counter += 1
