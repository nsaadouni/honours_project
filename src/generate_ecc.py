from fastecdsa import keys, curve
import binascii as ba

# generate a private key for curve P256
priv_key_1 = keys.gen_private_key(curve.P521)

# get the public key corresponding to the private key we just generated
pub_key_1 = keys.get_public_key(priv_key_1, curve.P521)
(Qx_1, Qy_1) = pub_key_1  # recall that pub_key is simply an integer pair

#---------------------------------------------------------------#

# generate a private key for curve P256
priv_key_2 = keys.gen_private_key(curve.P384)

# get the public key corresponding to the private key we just generated
pub_key_2 = keys.get_public_key(priv_key_2, curve.P384)
(Qx_2, Qy_2) = pub_key_2  # recall that pub_key is simply an integer pair

#---------------------------------------------------------------#

print len(hex(Qx_1)[2:-1] + hex(Qy_1)[2:-1])
print hex(Qx_1)[2:] #+ hex(Qy_1)[2:]
print ''
# print len(hex(Qx_2)[2:-1] + hex(Qy_2)[2:-1])
# print hex(Qx_2)[2:-1] + hex(Qy_2)[2:-1]
# print ''
