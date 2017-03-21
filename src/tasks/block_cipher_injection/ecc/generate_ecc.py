from fastecdsa import keys, curve
import binascii as ba

# generate a private key for curve P256
priv_key_1 = keys.gen_private_key(curve.P521)

# get the public key corresponding to the private key we just generated
pub_key_1 = keys.get_public_key(priv_key_1, curve.P521)
(Qx_1, Qy_1) = pub_key_1  # recall that pub_key is simply an integer pair

#---------------------------------------------------------------#

# generate a private key for curve P256
priv_key_2 = keys.gen_private_key(curve.P256)

# get the public key corresponding to the private key we just generated
pub_key_2 = keys.get_public_key(priv_key_2, curve.P256)
(Qx_2, Qy_2) = pub_key_2  # recall that pub_key is simply an integer pair

#---------------------------------------------------------------#


def intarray_to_hexstring(x):
	out = []
	for i in x:

		if i < 16:
			out.append('0'+hex(i)[2:-1])
		else:
			out.append(hex(i)[2:-1])

	out = ''.join(out)
	if len(out) % 2 == 0:
		return out
	else:
		return '0'+out

key1 = intarray_to_hexstring([Qx_1, Qy_1])
key2 = intarray_to_hexstring([Qx_2, Qy_2])

print key1
print len(key1)
print 'number of bytes = '+ str(len(key1)/2)

print ''

print key2
print len(key2)
print 'number of bytes = '+ str(len(key2)/2)

print ''

print intarray_to_hexstring([priv_key_2])
print len(intarray_to_hexstring([priv_key_2]))


print '\n\n\n\n\n\n\n\n\n\n'
print hex(Qx_1)[2:-1]
print ''
print hex(Qy_1)[2:-1]

print len(hex(Qx_1)[2:-1])
print len(hex(Qy_1)[2:-1])