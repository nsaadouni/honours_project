from PyKCS11 import *

def print_header(_str):
    print '*' * 60
    print ''
    print _str
    print ''


def generate_private_DES1_key(_id, _label):
    print_header('Generated private sensitive unextractable DES1 secret key "' + _label + '"')
    template = (
        (LowLevel.CKA_CLASS, LowLevel.CKO_PRIVATE_KEY),
        (LowLevel.CKA_KEY_TYPE, LowLevel.CKK_DES),
        (LowLevel.CKA_VALUE_LEN, 8),
        (LowLevel.CKA_LABEL, _label),
        (LowLevel.CKA_ID, chr(_id)),
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


def generate_private_DES2_key(_id, _label):
    print_header('Generated private sensitive unextractable DES2 secret key "' + _label + '"')
    template = (
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_DES2),
        (CKA_LABEL, _label),
        (CKA_ID, chr(_id)),
        (CKA_PRIVATE, True),
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
    m.mechanism = CKM_DES2_KEY_GEN
    key = LowLevel.CK_OBJECT_HANDLE()
    rv = pkcs11.lib.C_GenerateKey(session.session, m, t, key)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)


def generate_private_DES3_key(_id, _label):
    print_header('Generated private sensitive unextractable DES3 secret key "' + _label + '"')
    template = (
        (CKA_CLASS, CKO_SECRET_KEY),
        (CKA_KEY_TYPE, CKK_DES3),
        (CKA_LABEL, _label),
        (CKA_ID, chr(_id)),
        (CKA_PRIVATE, True),
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
    m.mechanism = CKM_DES3_KEY_GEN
    key = LowLevel.CK_OBJECT_HANDLE()
    rv = pkcs11.lib.C_GenerateKey(session.session, m, t, key)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)


# def generate_private_AES_key(_id, _label):
#     print_header('Generated private sensitive unextractable AES secret key "' + _label + '"')
#     template = (
#         (LowLevel.CKA_CLASS, LowLevel.CKO_SECRET_KEY),
#         (LowLevel.CKA_KEY_TYPE, LowLevel.CKK_AES),
#         (LowLevel.CKA_VALUE_LEN, 32),
#         (LowLevel.CKA_LABEL, _label),
#         (LowLevel.CKA_ID, chr(_id)),
#         (LowLevel.CKA_PRIVATE, True),
#         (LowLevel.CKA_SENSITIVE, True),
#         (LowLevel.CKA_ENCRYPT, True),
#         (LowLevel.CKA_DECRYPT, True),
#         (LowLevel.CKA_SIGN, True),
#         (LowLevel.CKA_VERIFY, True),
#         (LowLevel.CKA_TOKEN, True),
#         (LowLevel.CKA_WRAP, True),
#         (LowLevel.CKA_UNWRAP, True),
#         (LowLevel.CKA_EXTRACTABLE, False))
#     t = session._template2ckattrlist(template)
#     m = LowLevel.CK_MECHANISM()
#     m.mechanism = LowLevel.CKM_AES_KEY_GEN
#     key = LowLevel.CK_OBJECT_HANDLE()
#     rv = pkcs11.lib.C_GenerateKey(session.session, m, t, key)
#     # if rv != CKR_OK:
#     #     raise PyKCS11Error(rv)

def generate_private_AES_key(_id, _label):
    print_header('Generated private sensitive unextractable AES secret key "' + _label + '"')
    template = (
        (CKA_CLASS, LowLevel.CKO_PRIVATE_KEY),
        (CKA_KEY_TYPE, CKK_AES),
        (CKA_VALUE_LEN, 32),
        (CKA_LABEL, _label),
        (CKA_ID, chr(_id)),
        (CKA_PRIVATE, True),
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
    rv = pkcs11.lib.C_GenerateKey(session.session, m, t, key)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)

def generate_rsa_key_pair(_id, _label):
    print_header('Generated rsa key pair "' + _label[0] + '" and "' + _label[1] + '"')
    templatePub = (
        (CKA_ID, chr(_id)),
        (CKA_LABEL, _label[0]),
        (CKA_TOKEN, True),
        (CKA_PRIVATE, False),
        (CKA_ENCRYPT, True),
        (CKA_VERIFY, True),
        (CKA_WRAP, True),
        (CKA_MODULUS_BITS, 1024),
        (CKA_PUBLIC_EXPONENT, '\x01\x00\x01'))
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






print_header('initialize...')
lib = "/usr/lib/x64-athena/libASEP11.so"
pkcs11 = PyKCS11Lib()
pkcs11.load(lib)

print_header('login with pin "0000000000000000"...')
pin = '0000000000000000'
slot = pkcs11.getSlotList()[2]
session = pkcs11.openSession(slot, LowLevel.CKF_SERIAL_SESSION | LowLevel.CKF_RW_SESSION)
session.login(pin)

# generate_private_DES1_key(1, 'Apollo')

# generate_private_DES2_key(2, 'Ares')

# generate_private_DES3_key(3, 'Dionysus')

generate_private_AES_key(3, 'fucking_cunt')

# generate_rsa_key_pair(11, ['Odysseus', 'Penelope'])

# generate_rsa_key_pair(12, ['Eros', 'Psyche'])









#-------------------------------------------------------------------------------------------------------------------------
# modulus = [247, 181, 21, 114, 7, 34, 148, 111, 196, 8, 100, 203, 189, 175, 234, 85, 125, 189, 143, 85, 54, 176, 1, 194, 139, 46, 50, 182, 93, 69, 241, 116, 93, 56, 18, 11, 173, 157, 44, 3, 156, 34, 70, 104, 235, 46, 162, 140, 32, 149, 168, 46, 108, 168, 224, 109, 71, 242, 211, 30, 215, 1, 248, 21, 92, 173, 220, 5, 112, 192, 147, 178, 109, 116, 176, 155, 149, 230, 77, 140, 210, 252, 115, 62, 205, 15, 48, 104, 121, 165, 185, 53, 242, 65, 63, 82, 173, 173, 50, 160, 153, 26, 24, 61, 204, 87, 126, 57, 218, 71, 83, 30, 103, 21, 171, 1, 112, 127, 242, 71, 150, 113, 68, 35, 206, 123, 96, 103]

# private_exponent = [60, 82, 210, 6, 137, 40, 146, 44, 171, 230, 60, 78, 230, 223, 14, 210, 41, 241, 1, 190, 54, 196, 248, 84, 64, 86, 243, 74, 250, 141, 46, 155, 96, 245, 7, 188, 237, 180, 68, 86, 104, 93, 130, 76, 196, 234, 215, 150, 32, 248, 197, 70, 166, 224, 22, 184, 171, 165, 216, 67, 41, 88, 83, 119, 23, 9, 151, 170, 112, 104, 51, 158, 241, 65, 10, 95, 57, 217, 117, 36, 127, 58, 83, 99, 97, 71, 135, 135, 127, 136, 150, 188, 187, 131, 161, 203, 209, 66, 224, 235, 153, 207, 52, 14, 202, 86, 79, 44, 87, 80, 110, 123, 26, 252, 31, 144, 122, 224, 194, 168, 93, 211, 48, 227, 92, 169, 0, 57]

# create_rsa_private_key(15, 'Erebus', modulus, private_exponent)


# def create_rsa_private_key(_id, _label, _modulus, _private_exponent):
#     print_header('Created rsa private key "' + _label + '"')
#     template = (
#         (CKA_CLASS, CKO_PRIVATE_KEY),
#         (CKA_KEY_TYPE, CKK_RSA),
#         (CKA_ID, chr(_id)),
#         (CKA_LABEL, _label),
#         (CKA_MODULUS, _modulus),
#         (CKA_PRIVATE_EXPONENT, _private_exponent),
#         (CKA_TOKEN, True),
#         (CKA_PRIVATE, True),
#         (CKA_SENSITIVE, True),
#         (CKA_DECRYPT, True),
#         (CKA_SIGN, True),
#         (CKA_UNWRAP, True),
#         (CKA_EXTRACTABLE, False))
#     session.createObject(template)