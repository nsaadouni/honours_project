

from PyKCS11 import *



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
