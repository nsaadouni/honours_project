#!/usr/bin/python

import hashlib as hb 
import binascii

def print_all_hashes():
	for x in hb.algorithms_available:
		print(x)



def find_hash_used(x, y):

	# hb.algorithms_available
	# SHA-1, SHA-256, SHA-224, SHA-384, SHA-512
	# ['SHA', 'SHA1', 'SHA224', 'SHA384', 'SHA256', 'SHA512', 'DSA-SHA']
	for hash in hb.algorithms_available:
		h = hb.new(hash)
		h.update(str(x))
		hash_x_pin = h.hexdigest()
		check = int(hash_x_pin,16)
		# check = int(check % 2**(8*16))
		hash_x_pin = hex(check)[2:]
		if hash_x_pin == y:
			print("Hash found: " + hash)
			break
		else:
			print("Hash not found: " + hash)
			print 'calculcated hash: ' + str(hash_x_pin)
			print 'given hash      : ' + str(y)
			# print 'difference      : ' + str(y - check)
			print ''
			# pass

pin_0 = '12345'
pin_1 = '00000102030405'
pin_2 = '01020304050000'
pin_3 = '0012345'
pin_4 = '1234500'
pin_5 = '3039'

pin_0 = '313233343536'
pin_1 = '3132333435363030'
pin_2 = '3030313233343536'


x = '29C7291FED13237B'
y = 'AE69B84B7DBEBB2B6363D37D079DD3EC'

# print 'pin 1 integer: ' + str(int(pin_1,16))
# print 'pin 2 integer: ' + str(int(pin_2,16))
# print 'random number x integer: ' + str(int(x,16))
# print 'y calculated from x & pin: ' + str(int(y,16))
# print '---------------------------------'
# print ''

x_XOR_pin_0 = (int(x,16) ^ int(pin_0, 16))
x_XOR_pin_1 = (int(x,16) ^ int(pin_1, 16))
x_XOR_pin_2 = (int(x,16) ^ int(pin_2, 16))
# x_XOR_pin_3 = (int(x,16) ^ int(pin_3, 16))
# x_XOR_pin_4 = (int(x,16) ^ int(pin_4, 16))
# x_XOR_pin_5 = (int(x,16) ^ int(pin_5, 16)) 

x_con_pin_00 = int(x+pin_0,16)
x_con_pin_01 = int(pin_0+x,16)
x_con_pin_10 = int(x+pin_1,16)
x_con_pin_11 = int(pin_1+x,16)
x_con_pin_20 = int(x+pin_2,16)
x_con_pin_21 = int(pin_2+x,16)
# x_con_pin_30 = int(x+pin_3,16)
# x_con_pin_31 = int(pin_3+x,16)
# x_con_pin_40 = int(x+pin_4,16)
# x_con_pin_41 = int(pin_4+x,16)
# x_con_pin_50 = int(x+pin_5,16)
# x_con_pin_51 = int(pin_5+x,16)

yy = int(y,16)
yy = hex(yy)[2:]

find_hash_used(x_XOR_pin_0,yy)
find_hash_used(x_XOR_pin_1,yy)
find_hash_used(x_XOR_pin_2,yy)
# find_hash_used(x_XOR_pin_3,yy)
# find_hash_used(x_XOR_pin_4,yy)
# find_hash_used(x_XOR_pin_5,yy)

find_hash_used(x_con_pin_00,yy)
find_hash_used(x_con_pin_01,yy)
find_hash_used(x_con_pin_10,yy)
find_hash_used(x_con_pin_11,yy)
find_hash_used(x_con_pin_20,yy)
find_hash_used(x_con_pin_21,yy)
# find_hash_used(x_con_pin_30,yy)
# find_hash_used(x_con_pin_31,yy)
# find_hash_used(x_con_pin_40,yy)
# find_hash_used(x_con_pin_41,yy)
# find_hash_used(x_con_pin_50,yy)
# find_hash_used(x_con_pin_51,yy)

find_hash_used(int(pin_0,16)+int(x,16), yy)
find_hash_used(int(pin_1,16)+int(x,16), yy)
find_hash_used(int(pin_2,16)+int(x,16), yy)
# find_hash_used(int(pin_3,16)+int(x,16), yy)
# find_hash_used(int(pin_4,16)+int(x,16), yy)
# find_hash_used(int(pin_5,16)+int(x,16), yy)

find_hash_used(int(pin_0,16)-int(x,16), yy)
find_hash_used(int(pin_1,16)-int(x,16), yy)
find_hash_used(int(pin_2,16)-int(x,16), yy)
# find_hash_used(int(pin_3,16)-int(x,16), yy)
# find_hash_used(int(pin_4,16)-int(x,16), yy)
# find_hash_used(int(pin_5,16)-int(x,16), yy)

find_hash_used(int(pin_0,16)*int(x,16), yy)
find_hash_used(int(pin_1,16)*int(x,16), yy)
find_hash_used(int(pin_2,16)*int(x,16), yy)
# find_hash_used(int(pin_3,16)*int(x,16), yy)
# find_hash_used(int(pin_4,16)*int(x,16), yy)
# find_hash_used(int(pin_5,16)*int(x,16), yy)






#  29   C7   29   1F   ED   13   23   7B
# AE69 B84B 7DBE BB2B 6363 D37D 079D D3EC

# x_s = '129'
# y_s = 'ae69'

# t1 = '2900c70029001f01ed02130323047b05'
# t2 = '002900c70029011f02ed03130423057b'
# t3 = '2901c70229031f04ed05130023007b00'
# t4 = '012902c70329041f05ed00130023007b'

# xx = int(t4,16)
# yy = int(y,16)

# find_hash_used(xx,yy)