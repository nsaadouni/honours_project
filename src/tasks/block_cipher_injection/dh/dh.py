import binascii as ba
import sys
import hashlib as hs
from CryptoPlus.Cipher import DES, DES3



def hexstring_to_intarray(x):
    out = []
    if len(x) % 2 != 0:
        x = '0' + x

    for i in range(0,len(x), 2):
        out.append(int((x[i]+x[i+1]),16))
        # ba.unhexlify(x[i]+x[i+1])
    return out


def print_ints(command):

	for i in command:
		sys.stdout.write( str(i) +' ')
	print '\n'

# This changes!

public_api_intarray = [148, 107, 179, 115, 99, 253, 243, 11, 58, 110, 15, 68, 178, 233, 245, 171, 249, 2, 34, 214, 242, 130, 25, 76, 136, 163, 62, 226, 221, 149, 101, 19, 122, 239, 91, 108, 72, 15, 84, 195, 11, 76, 221, 22, 130, 144, 122, 249, 153, 186, 46, 130, 190, 45, 74, 225, 195, 255, 44, 75, 64, 195, 211, 15, 250, 68, 73, 243, 83, 63, 149, 232, 171, 163, 147, 150, 29, 165, 217, 72, 94, 192, 76, 29, 181, 132, 43, 140, 92, 159, 129, 124, 177, 8, 93, 94, 216, 136, 160, 128, 114, 107, 119, 73, 91, 69, 77, 100, 163, 95, 77, 161, 237, 240, 156, 23, 118, 202, 154, 17, 196, 8, 56, 170, 47, 221, 189, 188]

public_api = []
for i in public_api_intarray:
	if i < 16:
		public_api.append('0'+hex(i)[2:])
	else:
		public_api.append(hex(i)[2:])
public_api = int(''.join(public_api),16)

card_command = [128, 1, 5, 129, 129, 128, 247, 181, 21, 114, 7, 34, 148, 111, 196, 8, 100, 203, 189, 175, 234, 85, 125, 189, 143, 85, 54, 176, 1, 194, 139, 46, 50, 182, 93, 69, 241, 116, 93, 56, 18, 11, 173, 157, 44, 3, 156, 34, 70, 104, 235, 46, 162, 140, 32, 149, 168, 46, 108, 168, 224, 109, 71, 242, 211, 30, 215, 1, 248, 21, 92, 173, 220, 5, 112, 192, 147, 178, 109, 116, 176, 155, 149, 230, 77, 140, 210, 252, 115, 62, 205, 15, 48, 104, 121, 165, 185, 53, 242, 65, 63, 82, 173, 173, 50, 160, 153, 26, 24, 61, 204, 87, 126, 57, 218, 71, 83, 30, 103, 21, 171, 1, 112, 127, 242, 71, 150, 113, 68, 35, 206, 123, 96, 103, 130, 129, 128]
prime_intarray = [247, 181, 21, 114, 7, 34, 148, 111, 196, 8, 100, 203, 189, 175, 234, 85, 125, 189, 143, 85, 54, 176, 1, 194, 139, 46, 50, 182, 93, 69, 241, 116, 93, 56, 18, 11, 173, 157, 44, 3, 156, 34, 70, 104, 235, 46, 162, 140, 32, 149, 168, 46, 108, 168, 224, 109, 71, 242, 211, 30, 215, 1, 248, 21, 92, 173, 220, 5, 112, 192, 147, 178, 109, 116, 176, 155, 149, 230, 77, 140, 210, 252, 115, 62, 205, 15, 48, 104, 121, 165, 185, 53, 242, 65, 63, 82, 173, 173, 50, 160, 153, 26, 24, 61, 204, 87, 126, 57, 218, 71, 83, 30, 103, 21, 171, 1, 112, 127, 242, 71, 150, 113, 68, 35, 206, 123, 96, 103]
public_card_intarray = [60, 82, 210, 6, 137, 40, 146, 44, 171, 230, 60, 78, 230, 223, 14, 210, 41, 241, 1, 190, 54, 196, 248, 84, 64, 86, 243, 74, 250, 141, 46, 155, 96, 245, 7, 188, 237, 180, 68, 86, 104, 93, 130, 76, 196, 234, 215, 150, 32, 248, 197, 70, 166, 224, 22, 184, 171, 165, 216, 67, 41, 88, 83, 119, 23, 9, 151, 170, 112, 104, 51, 158, 241, 65, 10, 95, 57, 217, 117, 36, 127, 58, 83, 99, 97, 71, 135, 135, 127, 136, 150, 188, 187, 131, 161, 203, 209, 66, 224, 235, 153, 207, 52, 14, 202, 86, 79, 44, 87, 80, 110, 123, 26, 252, 31, 144, 122, 224, 194, 168, 93, 211, 48, 227, 92, 169, 0, 57]

# prime generation
prime = []
for i in prime_intarray:
	if i < 16:
		prime.append('0'+hex(i)[2:])
	else:
		prime.append(hex(i)[2:])

prime = int(''.join(prime), 16)

# public key of api generation
public_card = []
for i in public_card_intarray + []:
	if i < 16:
		public_card.append('0'+hex(i)[2:])
	else:
		public_card.append(hex(i)[2:])

public_card = int(''.join(public_card), 16)


generator = 5

# now we need to generate my own public key (it will remain constant)
priv_me = 0xffffffffffffffffffffffffffffffff

# now create my public key
public_me = pow(generator, priv_me, prime)


print 'public key Me -> API:\n'

print_my_pub = hexstring_to_intarray(hex(public_me)[2:-1])
p1 = card_command
for i in print_my_pub[0:129-9]:
	p1.append(i)
p1.append(97)
p1.append(9)
print_ints(p1)
print ''
p2 = print_my_pub[120:129]
p2.append(144)
p2.append(0)
print_ints(p2)

print '---------------------------------------'
print 'public key: Me -> Card \n'
p3 = [128,134,0,0,128]
for i in print_my_pub:
	p3.append(i)
p3.append(0)
print_ints(p3)



print 'My Challenge Me -> Card\n'
challenge = 'ff'*32
challenge = hexstring_to_intarray(challenge)
challenge.append(144)
challenge.append(0)
print_ints(challenge)


##############################################################
print '---------------------------------------'
print 'Shared secret S1: Me -> API'

# s1 = pow(public_card, priv_me, prime) # This is shared secret between me and CARD!
s1 = pow(public_api, priv_me, prime)
s1 = hex(s1)[2:-1]
s1_intarray = hexstring_to_intarray(s1)

s1_ascii = []
for i in s1_intarray:
	s1_ascii.append(chr(i))
s1_ascii = ''.join(s1_ascii)


s1_truncate_key1 = s1_ascii[0:16]

x = s1_ascii[16:32]
x = ba.hexlify(x)
x = hexstring_to_intarray(x)
s1_truncate_key2 =  []
for i in x:
	s1_truncate_key2.append(chr(i^0xff))
s1_truncate_key2 = ''.join(s1_truncate_key2)
# calculate MAC for apdu using key2

############################################################

h = hs.new('sha256')
h.update(s1_ascii)
s1_sha256 = h.digest() 

s1_sha256_key1 = s1_sha256[0:16]

x=ba.hexlify(s1_sha256[16:32])
x=hexstring_to_intarray(x)
s1_sha256_key2 = []
for i in x:
	s1_sha256_key2.append(chr(i^0xff))
s1_sha256_key2 = ''.join(s1_sha256_key2)

# calculate MAC for apdu using key2


API_20 = [12, 132, 0, 0, 13, 151, 1, 32, 142, 8, 237, 17, 224, 111, 191, 190, 148, 19, 0]
API_20_hex = []

for i in API_20:
	if i < 16:
		API_20_hex.append('0'+hex(i)[2:])
	else:
		API_20_hex.append(hex(i)[2:])

print ' '.join(API_20_hex)

CMAC = [237, 17, 224, 111, 191, 190, 148, 19]
cmac_digest = []
for i in CMAC:
	cmac_digest.append(chr(i))

cmac_digest = ''.join(cmac_digest)
print ba.hexlify(cmac_digest) + '\n'


msg1 = [12, 132, 0, 0,128,0,0,0, 128,0,0,0,0,0,0,0]

msg = []
for i in msg1:
	msg.append(chr(i))
msg = ''.join(msg)

# IVV = [150, 130, 205, 230, 219, 118, 196, 11]
IVV = [0,0,0,0,0,0,0,0]
IV = []
for i in IVV:
	IV.append(chr(i))
IV = ''.join(IV)

cipher1 = DES3.new(s1_truncate_key2, DES3.MODE_CBC, IV)
print ba.hexlify(cipher1.encrypt(msg))
cipher1 = DES3.new(s1_truncate_key2, DES3.MODE_CMAC, IV)
print ba.hexlify(cipher1.encrypt(msg))
cipher1 = DES3.new(s1_sha256_key2, DES3.MODE_CBC, IV)
print ba.hexlify(cipher1.encrypt(msg))
cipher1 = DES3.new(s1_sha256_key2, DES3.MODE_CMAC, IV)
print ba.hexlify(cipher1.encrypt(msg))




# print ''
# print ba.hexlify(s1_ascii)

# print ''
# print ba.hexlify(s1_truncate_key1)
# print ba.hexlify(s1_truncate_key2)
# print ba.hexlify(s1_sha256_key1)
# print ba.hexlify(s1_sha256_key2)