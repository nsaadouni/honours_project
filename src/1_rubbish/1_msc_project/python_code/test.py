from PyKCS11 import *


def print_header(_str):
    print '*' * 60
    print ''
    print _str
    print ''

print_header('initialize cryptoki...')

#initialize cryptoki
lib = '/usr/lib/x64-athena/libASEP11.so'
pkcs11 = PyKCS11Lib()
pkcs11.load(lib)
#print 'Initialization done.' 
#raw_input('Press Enter to continue...')

print_header('open session... (no trace for this part)')

#open session
slot = pkcs11.getSlotList()[0]
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
#print 'Session opened. No trace for this part.' 
#raw_input('Press Enter to continue...')

print_header('login in with pin "12345"...')

#login
pin = '0000000000000000'
session.login(pin)

template = (
    (CKA_CLASS, CKO_SECRET_KEY), 
    (CKA_LABEL, 'Hades_copy'))
t = session._template2ckattrlist(template)
rv = session.lib.C_FindObjectsInit(session.session, t)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
#print 'Finding objects initialized.'
#raw_input('Press Enter to continue...')

print_header('find the newly generated key... (no trace for this part)')

# find the generated secret key
result = PyKCS11.LowLevel.ckobjlist(1)
rv = session.lib.C_FindObjects(session.session, result)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
key = result[0]
print 'Found the generted secret key. No trace for this part.'
raw_input('Press Enter to continue...')

print_header('finalize finding objects... (no trace for this part)')

#finalize find objects (seems this section won't produce trace)
rv = session.lib.C_FindObjectsFinal(session.session)
if rv != CKR_OK:            
    raise PyKCS11Error(rv)
print 'Find objects terminated. No trace for this part.'
raw_input('Press Enter to continue...')

print_header('initialize encryption... (no trace for this part)')

#initialize encryption
mm = LowLevel.CK_MECHANISM()
mm.mechanism = CKM_AES_ECB
rv = session.lib.C_EncryptInit(session.session, mm, key)
if rv != CKR_OK: 
    raise PyKCS11Error(rv)
#print 'Encryption initialized. No trace for this part.'
#raw_input('Press Enter to continue...')

#prepare the data to encrypt
_data = 'abcdefghijklmnopqrstuvwxyz123456'
data = ckbytelist() 
data.reserve(32) 
for c in _data: 
    data.append(PyKCS11.byte_to_int(c)) 

print_header('get the size of encrypted message...')

#first call get encrypted size
encrypted = ckbytelist() 
rv = session.lib.C_Encrypt(session.session, data, encrypted)
rv = session.lib.C_Encrypt(session.session, data, encrypted)
print encrypted
print len(encrypted)

if rv != CKR_OK: 
    raise PyKCS11Error(rv)


#------------------------------------
#find the generated secret key
# session.login(pin)
# result2 = PyKCS11.LowLevel.ckobjlist(1)
# rv = session.lib.C_FindObjects(session.session, result2)
# if rv != CKR_OK:
#     raise PyKCS11Error(rv)
# key2 = result2[0]
# #print 'Found the generted secret key. No trace for this part.'
# #raw_input('Press Enter to continue...')
# print 'test'
# print_header('finalize finding objects... (no trace for this part)')

# #finalize find objects (seems this section won't produce trace)
# rv = session.lib.C_FindObjectsFinal(session.session)
# if rv != CKR_OK:            
#     raise PyKCS11Error(rv)

# mmm = LowLevel.CK_MECHANISM()
# mmm.mechanism = CKM_AES_ECB

# data1 = ckbytelist() 
# data1.reserve(32) 
# x = [156, 63, 100, 37, 19, 80, 104, 168, 86, 67, 148, 14, 205, 145, 163, 66, 171, 171, 189, 86, 224, 80, 232, 54, 243, 246, 103, 180, 56, 101, 100, 114]
# for i in x:
#     data1.append(i)

# rv = session.lib.C_DecryptInit(session.session, mmm, key2)
# if rv != CKR_OK: 
#     raise PyKCS11Error(rv)

# print_header('get the size of encrypted message...')

# #first call get encrypted size
# decrypted = ckbytelist() 
# rv = session.lib.C_Decrypt(session.session, data1, decrypted)
# rv = session.lib.C_Decrypt(session.session, data1, decrypted)
# print decrypted

# if rv != CKR_OK: 
#     raise PyKCS11Error(rv)
