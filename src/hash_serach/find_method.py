import math
# from bitarray import bitarray
import hashlib as hs 
import binascii as ba
from multiprocessing import Pool
import itertools

######################################################

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
#########################################################

# needs generalized to allow smaller and larger pins

def pad_end(pin, pad=255):
	out = []
	n = 16 - len(pin)
	for i in pin:
		out.append(i)
	for i in range(n):
		out.append(pad)

	return out

def pad_start(pin,pad=255):
	out = []
	n = 16 - len(pin)
	for i in range(n):
		out.append(pad)
	for i in pin:
		out.append(i)
	
	return out

##########################################################

def xor_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] ^ x_array[i])

 	return out

def nxor_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(~(pin_array[i] ^ x_array[i]) & 255)

 	return out

def or_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] | x_array[i])

 	return out

def nor_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append( (~(pin_array[i] | x_array[i])) & 255)

 	return out

def and_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] & x_array[i])

 	return out


def nand_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(~(pin_array[i] & x_array[i]) & 255)

 	return out


# NOTE: 255 == (2**8)-1

################################################################

def first_16_out(hexdigest):
	return hexdigest[:32]

def last_16_out(hexdigest):
	return hexdigest[-32:]

def mod_out(hexdigest):
	out = int(hexdigest,16)
	out = out % (2**(8*16))
	out = hex(out)[2:]
	if out[-1] == 'L':
		out = out[0:-1]

	if len(out) < 32:
		return '0' + out
	else:
		return out








#########################################################
#				Running Area							#
#########################################################
# ascii
pin = '12345'
# hex
X ='29 C7 29 1F ED 13 23 7B'
# hex
Y = 'AE 69 B8 4B 7D BE BB 2B 63 63 D3 7D 07 9D D3 EC'

# pre process inputs into lists
pin_list = []
for i in pin:
	pin_list.append(ord(i))

pin_int = intarray_to_hexstring(pin_list)
pin_int = int(pin_int,16)

X_list = []
for i in X.split():
	X_list.append(int(i,16))

X2 = ''.join(X.split())
X_int = int(X2,16)

Y_list = []
for i in Y.split():
	Y_list.append(int(i,16))


Y2 = ''.join(Y.split())
Y_int = int(Y2,16)
# Y2 = hex(Y2)[2:-1]

print ''
print 'pin: ' + pin
print 'pin list: ' + str(pin_list)
print 'pin list hex: ' + str(intarray_to_hexstring(pin_list))
print 'pin int: ' + str(pin_int)
print '--------------------------------------------'
print 'X: ' + X
print 'X2: ' + str(X2)
print 'X list: ' + str(X_list)
print 'X int: ' + str(X_int) 
print '--------------------------------------------'
print 'Y: ' + Y
print 'Y2: ' + Y2
print 'Y list: ' + str(Y_list)
print 'Y int: ' + str(Y_int)
print '--------------------------------------------'
print ''



"""

searches that need to be done

Joins are done byte by byte (which should be the same as it done as one integer) # test now [done]

i. hash joined pin and XX, reduce output to 16 bytes (2**128)
ii. hash joined pin_padded and XX, reduce output to 16 bytes
iii. hash pin, 


"""

def method_1(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)

	for i in intarray_to_asciiarray(X_list):
		h.update(i)

	t = join(p, hexstring_to_intarray(out(h.hexdigest())))

	return t, t == Y_list


def method_2(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)
	A = []
	for i in X_list:
		A.append(i)
	for i in X_list:
		A.append(i)

	_hashn = join(A, p)

	for i in intarray_to_asciiarray(_hashn):
		h.update(i)

	t = out(h.hexdigest())
	t = hexstring_to_intarray(t)

	return t, t == Y_list

def method_3(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad( pin_list, pad_i)

	_salted = []
	for i in p:
		_salted.append(i)
	for i in X_list:
		_salted.append(i)

	for i in intarray_to_asciiarray(_salted):
		h.update(i)

	t = hexstring_to_intarray(out(h.hexdigest()))

	return t, t == Y_list

def method_4(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)

	_salted = []
	for i in X_list:
		_salted.append(i)
	for i in p:
		_salted.append(i)

	for i in intarray_to_asciiarray(_salted):
		h.update(i)

	t = hexstring_to_intarray(out(h.hexdigest()))

	return t, t == Y_list

def method_5(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)

	_pnum = int(intarray_to_hexstring(p),16)
	_pnum += X_int

	_plist = hex(_pnum)[2:]
	if _plist[-1] == 'L':
		_plist = _plist[0:-1]

	_plist = hexstring_to_intarray(_plist)

	for i in intarray_to_asciiarray(_plist):
		h.update(i)

	t = hexstring_to_intarray(out(h.hexdigest()))

	return t, t == Y_list

def method_6(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)

	x2 = X_int**2
	x2_hex = hex(x2)[2:]
	if x2_hex[-1] == 'L':
		x2_hex = x2_hex[0:-1]
	x = hexstring_to_intarray(x2_hex)
	
	_hash = join(p, x)

	for i in intarray_to_asciiarray(_hash):
		h.update(i)

	t = hexstring_to_intarray(out(h.hexdigest()))

	return t, t == Y_list

def search_1():

	found = False
	c = 0

	joins = [xor_join, nxor_join, or_join, nor_join, and_join, nand_join]
	joins_str = ['xor', 'nxor', 'or', 'nor', 'and', 'nand']


	# methods = [method_1, method_2, method_3, method_4, method_5, method_6]
	# str_methods = ['method 1', 'method 2', 'method_3', 'method_4', 'method_5', 'method 6']
	methods = [method_7]
	str_methods = ['method 7']
	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']

	for join_index, join in enumerate(joins):
		for method_index, method in enumerate(methods):
			for pad_index, pad in enumerate(padding):
				for i in range(256):
					for hash_name in hs.algorithms_available:
						for out_index, out in enumerate(outputs):



							out, print_status = method(hash_name, pad, i, out, join)
							
							found = print_status

							if print_status:
								print 'FOUND YA BASTARD HAHAHAHAHAHA!'
								print 'method used: ' + str_methods[method_index]
								print 'padding is at the ' + padding_str[pad_index]
								print 'pad char (int): ' + str(i)
								print 'join used: ' + joins_str[join_index]
								print 'output format: ' + str_outputs[out_index]
								print 'hash name: ' + str(hash_name)
								print ''
								print Y_list
								print out
								print '--------------'
							elif out[0:2] == Y_list[0:2]:
								print ''
								print 'method used: ' + str_methods[method_index]
								print 'padding is at the ' + padding_str[pad_index]
								print 'pad char (int): ' + str(i)
								print 'join used: ' + joins_str[join_index]
								print 'output format: ' + str_outputs[out_index]
								print 'hash name: ' + str(hash_name)
								print ''
								print Y_list
								print out
								print '------------'
							c+=1
	
	print found	
	print c




# search_1()



def method_7(hash_name, pad, pad_i, rounds, out):

	h = hs.new(hash_name)
	if pad_i == 256:
		p = pin_list
	else:
		p = pad(pin_list, pad_i)

	password = []
	for i in intarray_to_asciiarray(p):
		password.append(i)
	password = ''.join(password)
	
	salt = []
	for i in intarray_to_asciiarray(X_list):
		salt.append(i)
	salt = ''.join(salt)

	dk = hs.pbkdf2_hmac(hash_name, password, salt, rounds)
	dkk = ba.hexlify(dk)
	t = hexstring_to_intarray(out(dkk))

	return t, t == Y_list



def search_2(hash_name):

	found = False
	c = 0

	methods = [method_7]
	str_methods = ['method 7']
	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(257):
			for rounds in range(1,100001):
				for out_index, out in enumerate(outputs):
				



					out, print_status = method_7(hash_name, pad, i, rounds, out)
					
					found = print_status

					if print_status:
						print 'FOUND YA BASTARD HAHAHAHAHAHA!'
						print 'padding is at the ' + padding_str[pad_index]
						print 'pad char (int): ' + str(i)
						print 'output format: ' + str_outputs[out_index]
						print 'hash name: ' + str(hash_name)
						print 'rounds: ' + str(i)
						print ''
						print Y_list
						print out
						print '--------------'
					elif 0:#out[0:2] == Y_list[0:2]:
						print ''
						print 'padding is at the ' + padding_str[pad_index]
						print 'pad char (int): ' + str(i)
						print 'output format: ' + str_outputs[out_index]
						print 'hash name: ' + str(hash_name)
						print 'rounds: ' + str(rounds)
						print ''
						print Y_list
						print out
						print '------------'
					c+=1
	
	print found	
	print c



_hashes = ['sha', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md4', 'md5', 'DSA-SHA', 'DSA', 'ecdsa-with-SHA1', 'ripemd160', 'whirlpool']
p = Pool(40)
p.map(search_2, _hashes)



# PARALLISE and run on university manchine





















#####################################################################
# test a join done seperately and a join done as one integer
# THEY ARE THE SAME!!!

# join done seperately

# j1 = nand_join(pad_end(pin_list,255), X_list)
# print j1

# p = pad_end(pin_list,255)
# p = intarray_to_hexstring(p)
# j2 = (~( int(p,16) & int(X2,16) )) & (2**(8*8) -1)
# # print hex(j2)
# print hexstring_to_intarray(hex(j2)[2:-1])







# # X squared
# 		# print int(out,16) + 9062629136450389448000026655859727641
# 		# print int(out,16) - 9062629136450389448000026655859727641
# 		# print int(out,16) ^ 9062629136450389448000026655859727641

# 		print hexstring_to_intarray(out)
# 		print xor_join(hexstring_to_intarray(out), Y_list)
# 		print Y_list
# 		# [65, 84, 72, 69, 78, 65, 83, 78, 192, 173, 170, 120, 252, 136, 66, 13]
# 		# ['A', 'T', 'H', 'E', 'N', 'A', 'S', 'N', '\xc0', '\xad', '\xaa', 'x', '\xfc', '\x88', 'B', '\r']


# 		# 16 bytes are read in a binary format from a file before get challenge is issued
# 		print ''
# 		ran = '41 54 48 45 4E 41 53 4E C0 AD AA 78 FC 88 42 0D'
#####################################################################