from PyKCS11 import *



"""
List of functions that I have to have traces for!!

session.login()
session.findObjects()
session.generateKeyPair() RSA
session.generateKey() BLOCK CIPHERS
session.createObject()
session.destroyObject()
session.encrypt()
session.decrypt()
session.sign()
session.verify()
session.__setattr__()
session.wrapKey()
session.unwrapKey()

new
getAttributeValue
getAttribute_value_fragmneted (returns None value when attribute is senseitive or unknown)
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


# incorrect at the minute
def generateKeyPair_rsa():
    templatePub = (
        (CKA_ID, '02'),
        (CKA_LABEL, 'test'),
        (CKA_TOKEN, False),
        (LowLevel.CKA_DERIVE, True),
        (LowLevel.CKA_VALUE_BITS, 521))
    templatePriv = (
        (CKA_ID, chr(_id)),
        (CKA_LABEL, _label[1]),
        (CKA_TOKEN, True),
        (CKA_PRIVATE, True),
        (CKA_SENSITIVE, True),
        (CKA_DECRYPT, True),
        (CKA_SIGN, True),
        (CKA_UNWRAP, True),
        (CKA_EXTRACTABLE, False))
    session.generateKeyPair(templatePub, templatePriv)
    return 0


# apparently block cipher keys should not require authentication!
# This doesnt make sense!
# PRIVATE == FALSE -> Works perfectly
def generate_AES(_id, label):
    arg = 0
    lib = "/usr/lib/x64-athena/libASEP11.so"
    pkcs11_aes = PyKCS11Lib()
    pkcs11_aes.load(lib)
    pin = '0000000000000000'


    slot = pkcs11_aes.getSlotList()[arg]
    session = pkcs11_aes.openSession(slot, LowLevel.CKF_SERIAL_SESSION | LowLevel.CKF_RW_SESSION)
    session.login(pin,1)

    template = (
        (LowLevel.CKA_CLASS, LowLevel.CKO_SECRET_KEY),
        (LowLevel.CKA_KEY_TYPE, LowLevel.CKK_AES),
        (LowLevel.CKA_VALUE_LEN, 32),
        (LowLevel.CKA_LABEL, label),
        (LowLevel.CKA_ID, _id),
        (CKA_ALWAYS_AUTHENTICATE, chr(2)),
        (LowLevel.CKA_PRIVATE, False),
        (LowLevel.CKA_SENSITIVE, True),
        (LowLevel.CKA_ENCRYPT, True),
        (LowLevel.CKA_DECRYPT, True),
        (LowLevel.CKA_TOKEN, True),
        (LowLevel.CKA_UNWRAP, False),
        (LowLevel.CKA_EXTRACTABLE, False))
    t = session._template2ckattrlist(template) 
    ck_handle = LowLevel.CK_OBJECT_HANDLE()
    m = LowLevel.CK_MECHANISM()
    m.mechanism = LowLevel.CKM_AES_KEY_GEN
    print LowLevel.CKM_AES_KEY_GEN
    rv = pkcs11_aes.lib.C_GenerateKey(session.session, m, t, ck_handle)
    if rv != LowLevel.CKR_OK:
        raise PyKCS11Error(rv) 
    return rv


def generate_DES(id, label):
    template = (
        (LowLevel.CKA_CLASS, LowLevel.CKO_SECRET_KEY),
        (LowLevel.CKA_KEY_TYPE, LowLevel.CKK_DES),
        (LowLevel.CKA_LABEL, label),
        (CKA_ID, "1224"),
        (LowLevel.CKA_PRIVATE, True),
        (LowLevel.CKA_SENSITIVE, True),
        (LowLevel.CKA_ENCRYPT, True),
        (LowLevel.CKA_DECRYPT, True),
        (LowLevel.CKA_SIGN, False),
        (LowLevel.CKA_VERIFY, False),
        (LowLevel.CKA_TOKEN, True),
        (LowLevel.CKA_UNWRAP, False),
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

# do not destroy the one block cipher key on there
def destroyAllObjects():
    objects = session.findObjects()
    for o in objects:
        _id = session.getAttributeValue(o, [LowLevel.CKA_ID])
        if _id[0][0] == 85:
            continue
        session.destroyObject(o)

########################################################
#                   Running Area                       #
########################################################

# arg = 2
# lib = "/usr/lib/x64-athena/libASEP11.so"
# pkcs11 = PyKCS11Lib()
# pkcs11.load(lib)
# pin = '0000000000000000'
# slot = pkcs11.getSlotList()[arg]
# session = pkcs11.openSession(slot, LowLevel.CKF_SERIAL_SESSION | LowLevel.CKF_RW_SESSION)
# session.login(pin,1)

# print pkcs11.getInfo()
# print ''



# Problem was PRITVATE -> apprently always neesd to be false! I.E do not need to authenticate

generate_AES("55", "aes_key_1")
# generate_DES(10, "deskey")


# print session.getSessionInfo()
# all_mecha =  pkcs11.getMechanismList(slot)
# for i in all_mecha:
#     print i

# destroyAllObjects()


# objects = session.findObjects()
# for i in objects:
#     attr = session.getAttributeValue(i, [LowLevel.CKA_VALUE_LEN])
#     print i
#     print '\n\n'

