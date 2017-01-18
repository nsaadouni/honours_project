#!/usr/bin/python

from PyKCS11 import *

def print_header(_str):
    print '*' * 60
    print ''
    print _str
    print ''

print_header('initialize cryptoki...')

#initialize cryptoki
lib = '/usr/lib/x86_64-linux-gnu/pkcs11-spy.so'
pkcs11 = PyKCS11Lib()
pkcs11.load(lib)
#print 'Initialization done.' 
#raw_input('Press Enter to continue...')

print_header('open session... (no trace for this part)')

#open session
slot = pkcs11.getSlotList()[-1]
session = pkcs11.openSession(slot, CKF_SERIAL_SESSION | CKF_RW_SESSION)
#print 'Session opened. No trace for this part.' 
#raw_input('Press Enter to continue...')

print_header('login in with pin "12345"...')

#login
pin = '12345'
session.login(pin)
#print 'Login with pin 12345.' 
#raw_input('Press Enter to continue...')

print_header('generate an AES secret key...')

#generate a 256 bit AES key
label = 'riddle'
template = (
    (CKA_CLASS, CKO_SECRET_KEY),
    (CKA_KEY_TYPE, CKK_AES),
    (CKA_VALUE_LEN, 32),
    (CKA_LABEL, label),
    (CKA_ID, '\x07'),
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
rv = pkcs11.lib.C_GenerateKey( session.session, m, t, key)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
#print 'secret key "riddle" generated.'
#raw_input('Press Enter to continue...')

print_header('generate another AES secret key...')

# generate another AES secret key 
label = 'maze'
template = (
    (CKA_CLASS, CKO_SECRET_KEY),
    (CKA_KEY_TYPE, CKK_AES),
    (CKA_VALUE_LEN, 32),
    (CKA_LABEL, label),
    (CKA_ID, '\x08'),
    (CKA_PRIVATE, False),
    (CKA_SENSITIVE, False),
    (CKA_ENCRYPT, True),
    (CKA_DECRYPT, True),
    (CKA_SIGN, True),
    (CKA_VERIFY, True),
    (CKA_TOKEN, True),
    (CKA_WRAP, True),
    (CKA_UNWRAP, True),
    (CKA_EXTRACTABLE, True))
t = session._template2ckattrlist(template)
key = LowLevel.CK_OBJECT_HANDLE()
rv = pkcs11.lib.C_GenerateKey( session.session, m, t, key)
if rv != CKR_OK:
    raise PyKCS11Error(rv)

print_header('initialize finding the newly generated key...')

#initialize find objects
template = (
    (CKA_CLASS, CKO_SECRET_KEY), 
    (CKA_LABEL, 'riddle'))
t = session._template2ckattrlist(template)
rv = session.lib.C_FindObjectsInit(session.session, t)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
#print 'Finding objects initialized.'
#raw_input('Press Enter to continue...')

print_header('find the newly generated key... (no trace for this part)')

#find the generated secret key
result = PyKCS11.LowLevel.ckobjlist(1)
rv = session.lib.C_FindObjects(session.session, result)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
key = result[0]
#print 'Found the generted secret key. No trace for this part.'
#raw_input('Press Enter to continue...')

print_header('finalize finding objects... (no trace for this part)')

#finalize find objects (seems this section won't produce trace)
rv = session.lib.C_FindObjectsFinal(session.session)
if rv != CKR_OK:            
    raise PyKCS11Error(rv)
#print 'Find objects terminated. No trace for this part.'
#raw_input('Press Enter to continue...')

print_header('initialize encryption... (no trace for this part)')

#initialize encryption
m.mechanism = CKM_AES_ECB
rv = session.lib.C_EncryptInit(session.session, m, key)
if rv != CKR_OK: 
    raise PyKCS11Error(rv)
#print 'Encryption initialized. No trace for this part.'
#raw_input('Press Enter to continue...')

#prepare the data to encrypt
_data = bytearray('abcdefghijklmnopqrstuvwxyz123456')
data = ckbytelist() 
data.reserve(32) 
for c in range(len(_data)): 
    data.append(_data[c]) 

print_header('get the size of encrypted message...')

#first call get encrypted size
encrypted = ckbytelist() 
rv = session.lib.C_Encrypt(session.session, data, encrypted) 
if rv != CKR_OK: 
    raise PyKCS11Error(rv)
#print 'Got the size of encrypted data.' 
#raw_input('Press Enter to continue...')

print_header('obtain the encrypted message...')
 
#second call get actual encrypted data 
rv = session.lib.C_Encrypt(session.session, data, encrypted) 
if rv != CKR_OK: 
    raise PyKCS11Error(rv) 
#print 'Got the encrypted data.'
#raw_input('Press Enter to continue...')

print_header('change the label of the generated secret key...')

#modify the label of the key
template = [(CKA_LABEL, 'Prometheus')]
t = session._template2ckattrlist(template)
rv = session.lib.C_SetAttributeValue(session.session, key, t)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
#print 'Set the label of the key to "Prometheus"'
#raw_input('Press Enter to continue...')

print_header('get the size of the new label of that secret key...')

#read the new label of the key
#first call to get the attribute size
attr = [CKA_LABEL]
valTemplate = PyKCS11.LowLevel.ckattrlist(len(attr)) 
for x in range(len(attr)): 
    valTemplate[x].SetType(attr[x])
rv = session.lib.C_GetAttributeValue(session.session, key, valTemplate) 
if rv != CKR_OK: 
    raise PyKCS11Error(rv)
#print 'Got the size of the new label.'
#raw_input('Press Enter to continue...')

print_header('read the new label of that secret key...')

#second call to get the attribute value 
rv = session.lib.C_GetAttributeValue(session.session, key, valTemplate) 
if rv != CKR_OK: 
    raise PyKCS11Error(rv)
label = valTemplate[0].GetString()
#print 'The new label is "' + label + '". No trace for this part.'
#raw_input('Press Enter to continue...')

print_header('generate a rsa key pair...')

#generate rsa key pair 'ice' and 'fire'
templatePub = (
    (CKA_ID, '\x03'),
    (CKA_LABEL, 'fire'),
    (CKA_TOKEN, True),
    (CKA_ENCRYPT, True),
    (CKA_VERIFY, True),
    (CKA_WRAP, True),
    (CKA_MODULUS_BITS, 1024),
    (CKA_PUBLIC_EXPONENT, '\x01\x00\x01'))
templatePriv = (
    (CKA_ID, '\x03'),
    (CKA_LABEL, 'ice'),
    (CKA_TOKEN, True),
    (CKA_PRIVATE, True),
    (CKA_SENSITIVE, True),
    (CKA_DECRYPT, True),
    (CKA_SIGN, True),
    (CKA_UNWRAP, True),
    (CKA_EXTRACTABLE, False))
keyPair = session.generateKeyPair(templatePub, templatePriv)
#print "RSA key pair generated."
#raw_input('Press Enter to continue...')

print_header('initialize signing... (no trace for this part)')

#initialize signature
key = keyPair[1]
m.mechanism = CKM_RSA_PKCS
rv = session.lib.C_SignInit(session.session, m, key)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
#print 'Signature initialized. No trace for this part.'
#raw_input('Press Enter to continue...')

#prepare the data to sign
_data = bytearray('Sign some data with the private key!')
data = ckbytelist()
data.reserve(len(_data))
for c in range(len(_data)):
    data.append(_data[c])

print_header('obtain the size of the signature...')

#first call get signature size
signature = ckbytelist()
rv = session.lib.C_Sign(session.session, data, signature)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
#print 'Got the size of the signature.'
#raw_input('Press Enter to continue...')

print_header('obtain the signature itself...')

#second call get signature itself
rv = session.lib.C_Sign(session.session, data, signature)
if rv != CKR_OK:
    raise PyKCS11Error(rv)
#print 'Got the signature data.'
#raw_input('Press Enter to continue...')

print_header('generate another pair of rsa key...')

#generate another rsa key pair 'pride' and 'prejudice'
templatePub = (
    (CKA_ID, '\x09'),
    (CKA_LABEL, 'pride'),
    (CKA_TOKEN, True),
    (CKA_ENCRYPT, True),
    (CKA_VERIFY, True),
    (CKA_WRAP, True),
    (CKA_MODULUS_BITS, 1024),
    (CKA_PUBLIC_EXPONENT, '\x01\x00\x01'))
templatePriv = (
    (CKA_ID, '\x09'),
    (CKA_LABEL, 'prejudice'),
    (CKA_TOKEN, True),
    (CKA_PRIVATE, False),
    (CKA_SENSITIVE, False),
    (CKA_DECRYPT, True),
    (CKA_SIGN, True),
    (CKA_UNWRAP, True),
    (CKA_EXTRACTABLE, True))
session.generateKeyPair(templatePub, templatePriv)
#print "RSA key pair 'pride' and 'prejudice' generated."
#raw_input('Press Enter to exit...')
