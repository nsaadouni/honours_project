from Crypto.Cipher import DES, DES3
import binascii as ba 

# input: array of characters (string)
# output: array of integers
def asciiarray_to_intarray(x):

	out = []
	for i in x:
		out.append(ord(i))
	return out

# input: array of integers
# output: array of ascii characters
def intarray_to_asciiarray(x):

	out = []
	for i in x:
		out.append(chr(i))
	return out

# input: array of integers
# output: string of hexidecimals
def intarray_to_hexstring(x):
	out = []
	for i in x:

		if i < 16:
			out.append('0'+hex(i)[2:])
		else:
			out.append(hex(i)[2:])

	# if out[-1] == 'L':
	# 	out = out[0:-1]
	return ''.join(out)

def hexstring_to_intarray(x):
	out = []
	if len(x) % 2 != 0:
		x = '0' + x

	for i in range(0,len(x), 2):
		out.append(int((x[i]+x[i+1]),16))
		# ba.unhexlify(x[i]+x[i+1])
	return out




# For DES try splitting the keys into 2 8 bytes
key1_des = '00000000'
key2_des = '00000000'
################################################################

#For DES3 XOR key2 with mask
key1_3des = '0000000000000000'
mask = [0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0]
key2_3des = []
for i in mask:
	key2_3des.append(chr(i^ord('0')))

key2_3des = ''.join(key2_3des)
################################################################

X = '00 00 00 00 00 00 00 00'
# X = 'd4 06 cb 15 79 4f 28 9f'
X = X.split()
msg = []
for i in X:
	msg.append(chr(int(i,16)))

msg = ''.join(msg)

###############################################################

IV = []
for i in range(8):
	IV.append(chr(0))

IV = ''.join(IV)

###############################################################

tmp = 'ce 62 54 20 d4 89 26 2f 59 57 0d e8 f7 f2 ca 08'
tmp = tmp.split()
ciphertext = []
for i in tmp:
	ciphertext.append(chr(int(i,16)))
ciphertext2 = ''.join(ciphertext)

##############################################################








# DES-MAC

cipher2 = DES3.new(key1_3des, DES3.MODE_CBC, IV)

ciphertext1 = cipher2.decrypt(ciphertext2)
conf = ciphertext1[0:8]
MAC = ciphertext1[8:16]

print ba.hexlify(conf)
print ba.hexlify(MAC)

# now from SKID2 repreduce MAC using:
# password, random number X, conf

print msg+conf
import hashlib
import hmac

for hash_used in hashlib.algorithms_available:
	h1 = hashlib.new(hash_used)
	h1.update(msg+conf)

	h2 = hashlib.new(hash_used)
	h2.update(conf+msg)

	print h1.hexdigest()
	print ''
	print h2.hexdigest()
	print ''

	# dig = hmac.new(key1_3des, msg+conf)


# cipher1 = DES3.new(key1_3des, DES3.MODE_CBC, IV)

# ciphertext11 = cipher1.encrypt(conf + msg)

# encrypted_conf = ciphertext11[0:8]
# MAC2 = ciphertext11[8:16]

# print ba.hexlify(MAC2)
# print ba.hexlify(encrypted_conf)