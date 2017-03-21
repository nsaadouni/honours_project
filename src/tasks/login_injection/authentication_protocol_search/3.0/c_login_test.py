# script for testing login hyptohises

from CryptoPlus.Cipher import DES3
import binascii as ba 
import hashlib as hs
"""
There is no cipher names DES2 -> therefore will have to use DES2 via key sizes!
What I am doign should defualt to DES due every character in the key being equal
"""

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

############################################

# These take in 2 array's of integers
def xor_join(Na, Nc):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] ^ x_array[i])

 	return out

def nxor_join(Na, Nc):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(~(pin_array[i] ^ x_array[i]) & 255)

 	return out

def or_join(Na, Nc):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] | x_array[i])

 	return out

def nor_join(Na, Nc):
 	out = []
 	for i in range(len(pin_array)):
 		out.append( (~(pin_array[i] | x_array[i])) & 255)

 	return out

def and_join(Na, Nc):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] & x_array[i])

 	return out

def nand_join(Na, Nc):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(~(pin_array[i] & x_array[i]) & 255)

 	return out

def hash_join(hash_name, Na, Nc):
	
	return 0
###########################################




"""
Returns all possibilites for the pin
pin, md5(pin), sha(pin), sha256(pin), sha512(pin)
truncated taking the first 16 bytes
"""
def pin_possibilities(pin, hash_functions):

	poss = []
	poss.append(pin)

	pin_int_array = asciiarray_to_intarray(pin)

	for i in hash_functions:
		h = hs.new(i)
		h.update(pin)
		poss.append(h.digest()[:16])

	return poss



"""
In this search we assumpe the following:
response = DES3-ECB(pin, msg=( Na|| Vnc ))
"""
def search(pin, challenge, response, hash_functions):
	
	all_pins = pin_possibilities(pin, hash_functions)
	all_bitwise_joins = [xor_join, xor_join, or_join, nor_join, and_join, nand_join]

	# 1. decrypt response -> Na || Vac
	# 2. 

	return 0






###############################################################################################################################
#												Running Area																  #
###############################################################################################################################



# pin = '0000000000000000'
# challenge = [0,0,0,0,0,0,0,0]
# resposne = [140, 100, 107, 145, 82, 161, 108, 33, 206, 244, 196, 50, 238, 13, 191, 47]
# hash_functions = ['md5', 'sha1', 'sha256', 'sha512']

# pins = pin_possibilities(pin, hash_functions)
# print pins



"""
----- APDU command/response pair 25 -----

COMMAND from API
00000000: 00 84 00 00 08                                    .....
[0, 132, 0, 0, 8]

Do you want to to alter command? (y/N)

RESPONSE
00000000: C1 FE 87 1E 27 A2 B2 C5  90 00                    ....'.....
[193, 254, 135, 30, 39, 162, 178, 197, 144, 0]

Do you want the response? (y/N)
y
Enter response (int array)
00 00 00 00 00 00 00 00 144 00
00000000: 00 00 00 00 00 00 00 00  90 00                    ..........
response changed!

----- APDU command/response pair 26 -----

COMMAND from API
00000000: 80 20 00 00 10 8C 64 6B  91 52 A1 6C 21 CE F4 C4  . ....dk.R.l!...
00000010: 32 EE 0D BF 2F                                    2.../
[128, 32, 0, 0, 16, 140, 100, 107, 145, 82, 161, 108, 33, 206, 244, 196, 50, 238, 13, 191, 47]


"""



# TEST 1

"""
00 00 00 00 00 00 00 00 90 00
50 0f c5 d2 ec 35 b8 eb 90 00

80 20 00 00 10 31 9c e9 78 1b bd d2 43 a6 8c e9 41 59 ff 70 c7
63 c9

00 00 00 00 00 00 00 00 90 00
ab a9 02 a5 e1 10 ea 44 90 00

80 20 00 00 10 31 9c e9 78 1b bd d2 43 a6 8c e9 41 59 ff 70 c7
63 c8

###################################################################
pin1 = 0000000000000000
pin2 = 1111111111111111

00 00 00 00 00 00 00 00 90 00
5b ab e8 bf a5 e9 c7 3e 90 00

80 20 00 00 10 84 af 5d 23 9f a8 2f d3 00 e2 95 46 1b e5 a4 d4
63 c7

00 00 00 00 00 00 00 00 90 00
65 d0 57 db f6 6f 6f 34 90 00

80 20 00 00 10 bd 2e e8 f6 0e 42 92 26 76 e4 5b 2d 9e 8a e7 30
63 c6

"""

# Test 2
"""
00 00 00 00 00 00 00 01 90 00
b2 98 e7 84 7e 5f 52 06 90 00

80 20 00 00 10 93 57 f7 53 42 a3 27 3d e6 b8 7e a6 81 98 5b 1c
63 c9

00 00 00 00 00 00 00 01 90 00
e0 5f fa a7 e6 bd 72 75 90 00

80 20 00 00 10 90 6a 74 d1 bd 2c 75 2e 52 ba 17 87 e3 70 51 ef
63 c8
"""


hash_functions = ['md5', 'sha1', 'sha256', 'sha512']
c = [0,0,0,0,0,0,0,0]
challenge = []
for i in c:
	challenge.append(chr(i))

r1 = '93 57 f7 53 42 a3 27 3d e6 b8 7e a6 81 98 5b 1c'
r1 = r1.split()
y1 = []
for i in r1:
	y1.append(chr(int(i,16)))
y1 = ''.join(y1)
pin1 = '0000000000000000'
all_pin1 = pin_possibilities(pin1, hash_functions)


r2 = '90 6a 74 d1 bd 2c 75 2e 52 ba 17 87 e3 70 51 ef'
r2 = r2.split()
y2 = []
for i in r2:
	y2.append(chr(int(i,16)))
y2 = ''.join(y2)

pin2 = '1111111111111111'
all_pin2 = pin_possibilities(pin2, hash_functions)

give_me = ['normal', 'md5', 'sha1', 'sha256', 'sha512']

pin1_c = 0
pin2_c = 0

for i in range(5):
		
		cipher = DES3.new(all_pin1[i], DES3.MODE_CBC, IV='\x00\x00\x00\x00\x00\x00\x00\x00')
		print ba.hexlify(cipher.decrypt(y1)[0:8]) + ' ' + ba.hexlify(cipher.decrypt(y1)[8:16])

		cipher = DES3.new(all_pin2[i], DES3.MODE_CBC, IV='\x00\x00\x00\x00\x00\x00\x00\x00')
		print ba.hexlify(cipher.decrypt(y2)[0:8]) + ' ' +  ba.hexlify(cipher.decrypt(y2)[8:16])

		print '\n pin method: ' + give_me[i]

		print '--------------------------------------------------------\n'




hash_sha1 = hs.new('sha1')
hash_sha1.update('0000000000000000')
password = hash_sha1.digest()[0:16]

y = '171 72 168 31 82 109 251 117 51 161 119 10 22 143 154 81'
y = '95 250 221 10 148 49 54 104 193 196 219 209 218 222 82 101'
y = y.split()
yy = []
for i in y:
	yy.append(chr(int(i)))
yy = ''.join(yy)

cipher = DES3.new(password, DES3.MODE_CBC, IV='\x00\x00\x00\x00\x00\x00\x00\x00')
a = ba.hexlify(cipher.decrypt(yy)[0:8])
b = ba.hexlify(cipher.decrypt(yy)[8:16])

print hexstring_to_intarray(a)
print hexstring_to_intarray(b)




