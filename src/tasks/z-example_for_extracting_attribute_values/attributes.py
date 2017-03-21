from PyKCS11 import *

pkcs11 = PyKCS11Lib()
pkcs11.load("/usr/lib/x64-athena/libASEP11.so")
slot = pkcs11.getSlotList()[2]
session = pkcs11.openSession(slot, PyKCS11.CKF_SERIAL_SESSION)

pin = '12345'
session.login(pin)


objects = session.findObjects()
all_attributes = [LowLevel.CKA_ALWAYS_AUTHENTICATE]
attrbibute_names = ['Always Authenticate'] 

for object in objects:
    try:
        attributes = session.getAttributeValue(object, all_attributes)
        print attributes
    except PyKCS11.PyKCS11Error as e:
        continue

    attrDict = dict(list(zip(all_attributes, attributes)))

    #if attrDict[PyKCS11.CKA_CERTIFICATE_CATEGORY] == (0x2, 0x0, 0x0, 0x0):
     #   continue

    #x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1,
     #                                       str(bytearray(attrDict[PyKCS11.CKA_VALUE])))



print all_attributes
