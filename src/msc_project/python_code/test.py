from PyKCS11 import *

pkcs11 = PyKCS11Lib()
pkcs11.load("/usr/lib/x64-athena/libASEP11.so")
slot = pkcs11.getSlotList()[2]
session = pkcs11.openSession(slot, PyKCS11.CKF_SERIAL_SESSION)
objects = session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_CERTIFICATE)])
all_attributes = [PyKCS11.CKA_SUBJECT, PyKCS11.CKA_VALUE, PyKCS11.CKA_ISSUER, PyKCS11.CKA_CERTIFICATE_CATEGORY, PyKCS11.CKA_END_DATE]

for object in objects:
    try:
        attributes = session.getAttributeValue(object, all_attributes)
    except PyKCS11.PyKCS11Error as e:
            continue

    attrDict = dict(list(zip(all_attributes, attributes)))

    if attrDict[PyKCS11.CKA_CERTIFICATE_CATEGORY] == (0x2, 0x0, 0x0, 0x0):
        continue

    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1,
                                            str(bytearray(attrDict[PyKCS11.CKA_VALUE])))

pin = '12345'
session.login(pin)