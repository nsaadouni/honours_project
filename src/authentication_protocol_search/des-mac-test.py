from CryptoPlus.Cipher import DES, DES3
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
tmp = '7c c0 e0 4c 14 1d 61 69 7f 7b b5 1e e0 fd 4f fb'
tmp = tmp.split()
ciphertext = []
for i in tmp:
	ciphertext.append(chr(int(i,16)))
ciphertext2 = ''.join(ciphertext)

##############################################################

# DES-MAC
print ''.join(tmp)[0:16] + ' ' + ''.join(tmp)[16:32]

cipher2 = DES3.new(key1_3des, DES3.MODE_ECB)

ciphertext1 = cipher2.decrypt(ciphertext2)
conf = ciphertext1[0:8]
MAC = ciphertext1[8:16]

print 'decrypted A: ' + ba.hexlify(conf)
print 'decrypted B: ' +ba.hexlify(MAC)
# print msg+conf

cipher1 = DES3.new(key1_3des, DES3.MODE_CMAC)

ciphertext11 = cipher1.encrypt(conf+msg)

encrypted_conf = ciphertext11[0:8]
MAC2 = ciphertext11[8:16]


print ba.hexlify(encrypted_conf)
print ba.hexlify(MAC2)





"""
3DES-ECB(key=pin, msg=Y) [decrypt] = [A||B]

3DES-CBC(key=pin, IV=A, msg=X) [encrypt] = A


"""


"""
SKID? -> was doing someting with that

DES && DES3 key = pin
Decrypt(16 bytes [Y]) -> ECB, CBC -> should give [conf, MAC]
Reproduce MAC using -> pin, X, conf!
"""