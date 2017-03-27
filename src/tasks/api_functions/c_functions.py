from PyKCS11 import *
import sys



# generateKeyPair RSA
def generateKeyPair_rsa(id='\x03', pub='pub', priv='priv', mod=1024):
    
    temp1 = (
        (CKA_ID, id),
        (CKA_LABEL, pub),
        (CKA_TOKEN, True),
        (CKA_PRIVATE, True),
        (CKA_ENCRYPT, True),
        (CKA_VERIFY, True),
        (CKA_WRAP, True),
        (CKA_MODULUS_BITS, mod),
        (CKA_PUBLIC_EXPONENT, '\x01\x00\x01'))
    
    temp2 = (
        (CKA_ID, id),
        (CKA_LABEL, priv),
        (CKA_TOKEN, True),
        (CKA_PRIVATE, True),
        (CKA_SENSITIVE, True),
        (CKA_DECRYPT, True),
        (CKA_SIGN, True),
        (CKA_UNWRAP, True),
        (CKA_EXTRACTABLE, True))
    session.generateKeyPair(temp1, temp2)


# generateKey AES
def generate_AES(id, label, private=False):
    template = (
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_AES),
        (CKA_VALUE_LEN, 32),
        (CKA_LABEL, label),
        (CKA_ID, id),
        (CKA_PRIVATE, private),
        (CKA_SENSITIVE, True),
        (CKA_ENCRYPT, True),
        (CKA_DECRYPT, True),
        (CKA_SIGN, True),
        (CKA_VERIFY, True),
        (CKA_TOKEN, True),
        (CKA_WRAP, True),
        (CKA_UNWRAP, True),
        (CKA_EXTRACTABLE, False))
    t = session._template2ckattrlist(template)
    m = LowLevel.CK_MECHANISM()
    m.mechanism = CKM_AES_KEY_GEN
    key = LowLevel.CK_OBJECT_HANDLE()
    rv = pkcs11.lib.C_GenerateKey( session.session, m, t, key)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)


# generateKey DES3
def generate_DES3(id, label, private=False):
    template = (
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_DES3),
        (CKA_LABEL, label),
        (CKA_ID, id),
        (CKA_PRIVATE, private),
        (CKA_SENSITIVE, True),
        (CKA_ENCRYPT, False),
        (CKA_DECRYPT, True),
        (CKA_SIGN, True),
        (CKA_VERIFY, True),
        (CKA_TOKEN, True),
        (CKA_UNWRAP, True),
        (CKA_EXTRACTABLE, False))
    t = session._template2ckattrlist(template)
    m = LowLevel.CK_MECHANISM()
    m.mechanism = CKM_DES3_KEY_GEN
    key = LowLevel.CK_OBJECT_HANDLE()
    rv = pkcs11.lib.C_GenerateKey( session.session, m, t, key)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)


# must use find object and pass the key 
def encrypt(id, label, mecha=CKM_DES3_ECB):

    template = (
    (CKA_CLASS, CKO_SECRET_KEY), 
    (CKA_LABEL, label),
    (CKA_ID, id))
    t = session._template2ckattrlist(template)

    rv = session.lib.C_FindObjectsInit(session.session, t)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)

    result = PyKCS11.LowLevel.ckobjlist(1)
    rv = session.lib.C_FindObjects(session.session, result)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    key = result[0]

    m = LowLevel.CK_MECHANISM()
    m.mechanism = mecha
    rv = session.lib.C_EncryptInit(session.session, m, key)
    
    if rv != CKR_OK: 
        raise PyKCS11Error(rv)

    data_to_encrypt='TestString123456'
    data = ckbytelist() 
    data.reserve(16) 
    for c in data_to_encrypt: 
        data.append(PyKCS11.byte_to_int(c))

    encrypted = ckbytelist() 
    rv = session.lib.C_Encrypt(session.session, data, encrypted)

    if rv != CKR_OK: 
        raise PyKCS11Error(rv)

    # decrypted = ckbytelist()
    rv = session.lib.C_Encrypt(session.session, data, encrypted)
    if rv != CKR_OK: 
        raise PyKCS11Error(rv)

    return encrypted


def decrypt(id, label, mecha=CKM_DES3_ECB):
    
    template = (
    (CKA_CLASS, CKO_SECRET_KEY), 
    (CKA_LABEL, label),
    (CKA_ID, id))
    t = session._template2ckattrlist(template)

    rv = session.lib.C_FindObjectsInit(session.session, t)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)

    result = PyKCS11.LowLevel.ckobjlist(1)
    rv = session.lib.C_FindObjects(session.session, result)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    key = result[0]

    m = LowLevel.CK_MECHANISM()
    m.mechanism = mecha

    data1 = ckbytelist() 
    data1.reserve(32)
    x =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,43, 20, 89, 72, 67, 8, 141, 45, 192, 249, 72, 237, 116, 128, 79, 1]

    for i in range(0, len(x)):
        data1.append(x[i])

    rv = session.lib.C_DecryptInit(session.session, m, key)
    if rv != CKR_OK: 
        raise PyKCS11Error(rv)

    decrypted = ckbytelist() 
    rv = session.lib.C_Decrypt(session.session, data1, decrypted)

    if rv != CKR_OK: 
        raise PyKCS11Error(rv)

    rv = session.lib.C_Decrypt(session.session, data1, decrypted)

    if rv != CKR_OK: 
        raise PyKCS11Error(rv)

    return decrypted


# provide key and template to change
def setAttribute(id, old_label, new_label):
    template = (
    (CKA_CLASS, CKO_SECRET_KEY), 
    (CKA_LABEL, old_label),
    (CKA_ID, id))
    t = session._template2ckattrlist(template)

    rv = session.lib.C_FindObjectsInit(session.session, t)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)

    result = PyKCS11.LowLevel.ckobjlist(1)
    rv = session.lib.C_FindObjects(session.session, result)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    key = result[0]

    rv = session.lib.C_FindObjectsFinal(session.session)
    if rv != CKR_OK:            
        raise PyKCS11Error(rv)

    template = [(CKA_LABEL, new_label)]
    t = session._template2ckattrlist(template)
    rv = session.lib.C_SetAttributeValue(session.session, key, t)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)



# step 1 to finding an object (SECRET KEY OBJECT)
def findObjectsInit(id, label):
    template = (
    (CKA_CLASS, CKO_SECRET_KEY), 
    (CKA_LABEL, label),
    (CKA_ID, id))
    t = session._template2ckattrlist(template)

    rv = session.lib.C_FindObjectsInit(session.session, t)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)

# step 2 locate and finialise object
def finaliseObject():
    result = PyKCS11.LowLevel.ckobjlist(1)
    rv = session.lib.C_FindObjects(session.session, result)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    key = result[0]

    rv = session.lib.C_FindObjectsFinal(session.session)
    if rv != CKR_OK:            
        raise PyKCS11Error(rv)
    
    return key




#--------------------------------------------------------#


def destroyAllObjects():
    objects = session.findObjects()
    for o in objects:
        session.destroyObject(o)


def print_mechlist():
    print session.getSessionInfo()
    all_mecha =  pkcs11.getMechanismList(slot)
    for i in all_mecha:
        print i

def attribute_hex_values():

    attributes_int = [CKA_ALWAYS_AUTHENTICATE,
    CKA_ALWAYS_SENSITIVE, CKA_CLASS, CKA_DECRYPT, CKA_DERIVE, CKA_ENCRYPT, CKA_END_DATE, CKA_EXTRACTABLE,
    CKA_ID, CKA_KEY_GEN_MECHANISM, CKA_KEY_TYPE, CKA_LABEL, CKA_LOCAL, CKA_MODIFIABLE, CKA_NEVER_EXTRACTABLE, 
    CKA_PRIVATE, CKA_SENSITIVE, CKA_SIGN, CKA_START_DATE, CKA_TOKEN ,CKA_UNWRAP, CKA_VALUE ,CKA_VERIFY ,CKA_WRAP]

    attributes = ['CKA_ALWAYS_AUTHENTICATE',
    'CKA_ALWAYS_SENSITIVE', 'CKA_CLASS', 'CKA_DECRYPT', 'CKA_DERIVE', 'CKA_ENCRYPT', 'CKA_END_DATE', 'CKA_EXTRACTABLE',
    'CKA_ID', 'CKA_KEY_GEN_MECHANISM', 'CKA_KEY_TYPE', 'CKA_LABEL', 'CKA_LOCAL', 'CKA_MODIFIABLE', 'CKA_NEVER_EXTRACTABLE', 
    'CKA_PRIVATE', 'CKA_SENSITIVE', 'CKA_SIGN', 'CKA_START_DATE', 'CKA_TOKEN' ,'CKA_UNWRAP', 'CKA_VALUE' ,'CKA_VERIFY',
    'CKA_WRAP']

    for i in range(len(attributes)):
        print attributes[i] + '\t\t' + hex(attributes_int[i])


########################################################
#                   Running Area                       #
########################################################

# arg = int(sys.argv[1])
# lib = "/usr/lib/x64-athena/libASEP11.so"
# pkcs11 = PyKCS11Lib()
# pkcs11.load(lib)
# pin = '0000000000000000'
# slot = pkcs11.getSlotList()[arg]
# session = pkcs11.openSession(slot, LowLevel.CKF_SERIAL_SESSION | LowLevel.CKF_RW_SESSION)
# session.login(pin,1)


attribute_hex_values()
print '\n'



# generate_AES('\x00', 'aes')
# generate_DES3('\x01', 'des3')
# generateKeyPair_rsa()

# setAttribute('\x01', 'des3', 'changed')
# setAttribute('\x01', 'changed', 'des3')

# findObjectsInit('\x01', 'des3')
# keyobject = finaliseObject()

# encrypted_text= encrypt('\x05', 'ef', CKM_DES_ECB)
# print encrypted_text
# decrypted_text = decrypt('\x00', 'aes' , CKM_AES_ECB)
# print decrypted_text

# out = []
# for i in decrypted_text:
#     out.append(chr(i))
# print ''.join(out)



# destroyAllObjects()

# generate_AES('\x00', 'aes')

# generateKeyPair_rsa()


# template = (
#     (CKA_CLASS, CKO_PUBLIC_KEY),
#     (CKA_LABEL, 'pub'),
#     (CKA_ID, '\x03'))
# temp = session._template2ckattrlist(template)
# keys = session.findObjects()
# print session.encrypt(keys[0], '12345678')


# objects = session.findObjects()
# key_to_unwrap = session.encrypt(objects[0], '12345678')
# template = (
#         (CKA_CLASS, CKO_SECRET_KEY),
#         (CKA_KEY_TYPE, CKK_DES),
#         (CKA_LABEL, 'test3'),
#         (CKA_ID, '\x12'),
#         (CKA_PRIVATE, True),
#         (CKA_SENSITIVE, True),
#         (CKA_ENCRYPT, True),
#         (CKA_DECRYPT, True),
#         (CKA_SIGN, True),
#         (CKA_VERIFY, True),
#         (CKA_TOKEN, True),
#         (CKA_UNWRAP, True),
#         (CKA_EXTRACTABLE, False))
# temp = session._template2ckattrlist(template)


# print 'test'
# print session.unwrapKey(objects[1],key_to_unwrap, template)

# generate_DES3('\x15', 'ef')
# encrypted_text= encrypt('\x15', 'ef', CKM_DES_ECB)
# print encrypted_text

# objects = session.findObjects()
# for i in objects:
#     print i
#     print ''



