import math
import hashlib as hs 
import binascii as ba

from multiprocessing import Pool
import itertools


"""
ALL OF THIS CODE NEEDS CLEANED UP TODAY
I ALSO NEED A FULL EXPLANATION OF WHAT EXACTLY HAS BEEN DONE HERE!
"""

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

def invert_intarray(x):
	out = []
	for i in x:
		out.append((~i) & 255)

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
pin = '0000000000000000'
# hex
X ='29 C7 29 1F ED 13 23 7B'
X = '68 F1 E4 92 85 36 39 A3'
# hex
Y = 'AE 69 B8 4B 7D BE BB 2B 63 63 D3 7D 07 9D D3 EC'
Y  = '53 17 55 20 F4 30 18 56 80 E6 75 55 E1 91 A7 EC'

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

Y_list_invert = invert_intarray(Y_list)


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
print 'Y list inverted: ' + str(Y_list_invert)
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

"""
hash X -> 16 bytes
join hash(X) and pin 
"""
def method_1(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)

	for i in intarray_to_asciiarray(X_list):
		h.update(i)

	t = join(p, hexstring_to_intarray(out(h.hexdigest())))

	return t, t == Y_list

"""
HASH(join(pin , X||X))
reduce to 16 bytes
"""
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

"""
salt pin with X (pin comes first)
hash salted pin
"""
def method_3(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)
	# p = pin_list

	_salted = []
	for i in p:
		_salted.append(i)
	for i in X_list:
		_salted.append(i)

	for i in intarray_to_asciiarray(_salted):
		h.update(i)

	t = hexstring_to_intarray(out(h.hexdigest()))

	return t, t == Y_list

"""
salt pin with X (X comes first)
hash salted pin
"""
def method_4(hash_name, pad, pad_i, out, join):

	h = hs.new(hash_name)
	p = pad(pin_list, pad_i)
	# p = pin_list

	_salted = []
	for i in X_list:
		_salted.append(i)
	for i in p:
		_salted.append(i)

	for i in intarray_to_asciiarray(_salted):
		h.update(i)

	t = hexstring_to_intarray(out(h.hexdigest()))

	return t, t == Y_list

"""
format pin to integer
pin += random number (from get challenge)
hash 
"""
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
	# t = _plist

	return t, t == Y_list

"""
square(random number) (creates 16 bytes) becuase (2^(8*16))^2 == 2^16*16
use the join methods (xor, nxor etc...) to join(pin, square(x))
hash 
"""
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
	# t = _hash

	return t, t == Y_list



def search_1():

	found = False
	c = 0

	joins = [xor_join, nxor_join, or_join, nor_join, and_join, nand_join]
	joins_str = ['xor', 'nxor', 'or', 'nor', 'and', 'nand']


	methods = [method_1, method_2, method_3, method_4, method_5, method_6]
	str_methods = ['method 1', 'method 2', 'method_3', 'method_4', 'method_5', 'method 6']
	# methods = [method_7]
	# str_methods = ['method 7']
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



							o, print_status = method(hash_name, pad, i, out, join)
							
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
								print o
								print '--------------'
							elif o[0:2] == Y_list_invert[0:2]:
								print ''
								print 'method used: ' + str_methods[method_index]
								print 'padding is at the ' + padding_str[pad_index]
								print 'pad char (int): ' + str(i)
								print 'join used: ' + joins_str[join_index]
								print 'output format: ' + str_outputs[out_index]
								print 'hash name: ' + str(hash_name)
								print ''
								print Y_list
								print o
								print '------------'
							c+=1
	
	print found	
	print c




# search_1()



def method_7(hash_name, pad, pad_i, rounds):

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

	dk = hs.pbkdf2_hmac(hash_name, password, salt, rounds, 16)
	dkk = ba.hexlify(dk)
	t = hexstring_to_intarray(dkk)

	return t, t == Y_list



def search_2(hash_name):

	found = False
	c = 0

	methods = [method_7]
	str_methods = ['method 7']
	# padding = [pad_end, pad_start]
	padding = [pad_end]
	padding_str = ['END', 'START']

	pads = [0, 255, 256]

	for rounds in range(1,10001):
		for pad_index, pad in enumerate(padding):
			for i in range(257):

				out, print_status = method_7(hash_name, pad, i, rounds)
				
				found = print_status

				if print_status:
					print 'FOUND YA BASTARD HAHAHAHAHAHA!'
					print 'padding is at the ' + padding_str[pad_index]
					print 'pad char (int): ' + str(i)
					print 'hash name: ' + str(hash_name)
					print 'rounds: ' + str(i)
					print ''
					print Y_list
					print out
					print '--------------'
				elif out[0:2] == Y_list_invert[0:2]:
					print ''
					print 'padding is at the ' + padding_str[pad_index]
					print 'pad char (int): ' + str(i)
					print 'hash name: ' + str(hash_name)
					print 'rounds: ' + str(rounds)
					print ''
					print Y_list_invert
					print out
					print '------------'
				# else:
					# print 'rounds :' + str(rounds)
				c+=1

	print found	
	print c



# _hashes = ['sha', 'sha1', 'sha256']# 'sha224', 'sha256', 'sha384', 'sha512', 'md4', 'md5', 'DSA-SHA', 'DSA', 'ecdsa-with-SHA1', 'ripemd160', 'whirlpool']
# p = Pool(3)
# p.map(search_2, _hashes)



# PARALLISE and run on university manchine

import hmac

def search_3():

	found = False
	c = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(257):
			for hash_name in [hs.sha1, hs.sha224, hs.sha256, hs.sha384, hs.sha512, hs.md5]:
				for out_index, out in enumerate(outputs):

					if i == 256:
						p = pin_list
					else:
						p = pad(pin_list, i)

					# dig = hmac.new(''.join(intarray_to_asciiarray(p)), msg=''.join(intarray_to_asciiarray(X_list)), digestmod=hash_name)
					# dig = hmac.new(''.join(intarray_to_asciiarray(X_list)),''.join(intarray_to_asciiarray(p)), digestmod=hash_name)

					
					key = ''.join(intarray_to_asciiarray(p))
					password = ''.join(intarray_to_asciiarray(X_list))
					# print key
					# print password
					# print ''
					dig = hmac.new(password, key, hash_name)
					d = out(dig.hexdigest())
					d = hexstring_to_intarray(d)
					
					found = d == Y_list

					if found:
						print 'FOUND YA BASTARD HAHAHAHAHAHA!'
						# print 'method used: ' + str_methods[method_index]
						print 'padding is at the ' + padding_str[pad_index]
						print 'pad char (int): ' + str(i)
						# print 'join used: ' + joins_str[join_index]
						print 'output format: ' + str_outputs[out_index]
						print 'hash name: ' + str(hash_name)
						print ''
						print Y_list
						print d
						print '--------------'
					elif d[0] == Y_list [0]:
						print ''
						# print 'method used: ' + str_methods[method_index]
						print 'padding is at the ' + padding_str[pad_index]
						print 'pad char (int): ' + str(i)
						# print 'join used: ' + joins_str[join_index]
						print 'output format: ' + str_outputs[out_index]
						print 'hash name: ' + str(hash_name)
						print ''
						print Y_list
						print Y_list_invert
						print d
						print '------------'
					c+=1
	
	print found	
	print c



# search_3()






from Crypto.Cipher import AES

def search_4():

	found = False
	counter = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	# outputs = [first_16_out, last_16_out, mod_out]
	# str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(256):

			hash_name = 'sha256'
			h = hs.new(hash_name)

			X = intarray_to_asciiarray(X_list)
			for j in X:
				h.update(j)

			p = pad(pin_list,i)
			pin_ascii = intarray_to_asciiarray(p)

			msg = h.digest()
			AES_key = ''.join(pin_ascii)
			obj = AES.new(AES_key, AES.MODE_CBC, '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')

			c = obj.encrypt(msg)
			c_hex = ba.b2a_hex(c)
			c_list = hexstring_to_intarray(c_hex)
			
			found = Y_list_invert == c_list

			if Y_list[0] == c_list[0]:

				print p
				print c_list
				print Y_list
				print '------------------------'
				print ''

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				# print 'method used: ' + str_methods[method_index]
				print 'padding is at the ' + padding_str[pad_index]
				print 'pad char (int): ' + str(i)
				# print 'join used: ' + joins_str[join_index]
				# print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print out
				print '--------------'
			
			# elif out[0:2] == Y_list[0:2]:
			# 	print ''
			# 	print 'method used: ' + str_methods[method_index]
			# 	print 'padding is at the ' + padding_str[pad_index]
			# 	print 'pad char (int): ' + str(i)
			# 	print 'join used: ' + joins_str[join_index]
			# 	print 'output format: ' + str_outputs[out_index]
			# 	print 'hash name: ' + str(hash_name)
			# 	print ''
			# 	print Y_list
			# 	print out
			# 	print '------------'
			counter+=1
	
	print found	
	print counter

# search_4()

def search_5():

	found = False
	counter = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	# outputs = [first_16_out, last_16_out, mod_out]
	# str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(256):

			hash_name = 'sha256'
			h = hs.new(hash_name)

			X = intarray_to_asciiarray(X_list)
			for j in X:
				h.update(j)

			IVV = hexstring_to_intarray(h.hexdigest())
			IVV = intarray_to_asciiarray(IVV)
			IV = IVV[0:16]
			IV = ''.join(IV)

			p = pad(pin_list,i)
			pin_ascii = intarray_to_asciiarray(p)

			AES_key = ''.join(pin_ascii)
			obj = AES.new(AES_key, AES.MODE_CBC, IV)

			msg = IVV[16:32]
			# msg = intarray_to_asciiarray(msg)
			msg = ''.join(msg)
			c = obj.encrypt(msg)
			c_hex = ba.b2a_hex(c)
			c_list = hexstring_to_intarray(c_hex)

			c1 = c_list[0:16]
			# c2 = c_list[16:32]
			
			found = c1 == Y_list

			if c1[0] == Y_list_invert[0]:
				print p
				print c1
				# print c2
				print Y_list
				print '------------------------'
				print ''

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				# print 'method used: ' + str_methods[method_index]
				print 'padding is at the ' + padding_str[pad_index]
				print 'pad char (int): ' + str(i)
				# print 'join used: ' + joins_str[join_index]
				# print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print out
				print '--------------'
			
			# elif out[0:2] == Y_list[0:2]:
			# 	print ''
			# 	print 'method used: ' + str_methods[method_index]
			# 	print 'padding is at the ' + padding_str[pad_index]
			# 	print 'pad char (int): ' + str(i)
			# 	print 'join used: ' + joins_str[join_index]
			# 	print 'output format: ' + str_outputs[out_index]
			# 	print 'hash name: ' + str(hash_name)
			# 	print ''
			# 	print Y_list
			# 	print out
			# 	print '------------'
			counter+=1
	
	print found	
	print counter


# search_5()






from CryptoPlus.Cipher import AES

def search_6():

	found = False
	counter = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	# outputs = [first_16_out, last_16_out, mod_out]
	# str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(256):

			p = pad(pin_list,i)
			pin_ascii = intarray_to_asciiarray(p)
			key = ''.join(pin)
			
			ci = AES.new(key, AES.MODE_CMAC)

			msg = intarray_to_asciiarray(X_list)
			msg = ''.join(msg)

			cit = ci.encrypt(msg).encode('hex')
			cit = hexstring_to_intarray(cit)

			
			if cit[0] == Y_list[0]:
				print p
				print cit
				print Y_list
				print '------------------------'
				print ''

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				# print 'method used: ' + str_methods[method_index]
				print 'padding is at the ' + padding_str[pad_index]
				print 'pad char (int): ' + str(i)
				# print 'join used: ' + joins_str[join_index]
				# print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print out
				print '--------------'
			counter+=1
	
	print found	
	print counter



# search_6()




def search_7():

	found = False
	counter = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	# outputs = [first_16_out, last_16_out, mod_out]
	# str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(257):

			if i == 256:
				p = pin_list
			else:
				p = pad(pin_list,i)

			pin_ascii = intarray_to_asciiarray(p)
			msg = ''.join(pin_ascii)
			
			XX_list = []
			for i in X_list:
				XX_list.append(i)
			for i in X_list:
				XX_list.append(i)

			key = intarray_to_asciiarray(XX_list)
			key = ''.join(key)
			

			ci = AES.new(key, AES.MODE_CMAC)
			cit = ci.encrypt(msg).encode('hex')
			cit = hexstring_to_intarray(cit)

			
			if cit[0] == Y_list_invert[0]:
				print p
				print cit
				print Y_list
				print '------------------------'
				print ''

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				# print 'method used: ' + str_methods[method_index]
				print 'padding is at the ' + padding_str[pad_index]
				print 'pad char (int): ' + str(i)
				# print 'join used: ' + joins_str[join_index]
				# print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print out
				print '--------------'
			counter+=1
	
	print found	
	print counter



# search_7()



def search_8():

	found = False
	counter = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	# outputs = [first_16_out, last_16_out, mod_out]
	# str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(257):

			h = hs.sha256()

			if i == 256:
				p = pin_list
			else:
				p = pad(pin_list,i)
			pin_ascii = intarray_to_asciiarray(p)
			pin_ascii = ''.join(pin_ascii)
			h.update(pin_ascii)

			key = h.digest()

			# print len(key)
			
			ci = AES.new(key, AES.MODE_CMAC)

			msg = intarray_to_hexstring(X_list)
			msg = ''.join(msg)

			cit = ci.encrypt(msg).encode('hex')
			cit = hexstring_to_intarray(cit)

			found = cit == Y_list

			
			if cit[0] == Y_list_invert[0]:
				print p
				print cit
				print Y_list_invert
				# print 'key: ' + key
				print '------------------------'
				print ''

			if cit[0] == Y_list[0]:
				print p
				print cit
				print Y_list
				print '------------------------'
				print ''

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				# print 'method used: ' + str_methods[method_index]
				print 'padding is at the ' + padding_str[pad_index]
				print 'pad char (int): ' + str(i)
				# print 'join used: ' + joins_str[join_index]
				# print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print out
				print '--------------'
			counter+=1
	
	print found	
	print counter


# search_8()



from Crypto.Cipher import DES3


def search_9():

	found = False
	counter = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	# outputs = [first_16_out, last_16_out, mod_out]
	# str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(256):

			# p = pad(pin_list, i)
			# pin_ascii = intarray_to_asciiarray(p)
			key = ''.join(pin)

			msg = intarray_to_asciiarray(X_list)
			msg = ''.join(msg)

			# print len(key)
			
			ci = DES3.new(key, DES3.MODE_ECB, '\x00\x00\x00\x00\x00\x00\x00\x00')

			cit = ci.encrypt(msg).encode('hex')
			cit = hexstring_to_intarray(cit)

			found = cit == Y_list

			
			if cit[0] == Y_list_invert[0]:
				print p
				print cit
				print Y_list_invert
				# print 'key: ' + key
				print '------------------------'
				print ''

			if cit[0] == Y_list[0]:
				print p
				print cit
				print Y_list
				print '------------------------'
				print ''

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				# print 'method used: ' + str_methods[method_index]
				print 'padding is at the ' + padding_str[pad_index]
				print 'pad char (int): ' + str(i)
				# print 'join used: ' + joins_str[join_index]
				# print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print out
				print '--------------'
			counter+=1
	
	print found	
	print counter


# search_9()





def search_10():

	found = False
	c = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']


	for hash_name in [hs.sha1, hs.sha224, hs.sha256, hs.sha384, hs.sha512, hs.md5]:
		for hn in hs.algorithms_available:

			h1 = hs.new(hn)
			h1.update(pin)
			hashed_password = h1.digest()
			
			key = ''.join(intarray_to_asciiarray(X_list))

			dig = hmac.new(password, key, hash_name)
			d = out(dig.hexdigest())
			d = hexstring_to_intarray(d)
			
			found = d == Y_list

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				print ''
				print Y_list
				print d
				print '--------------'
			elif d[0] == Y_list [0]:
				print 'something relevant'
				print ''
				print Y_list
				print Y_list_invert
				print d
				print '------------'
			c+=1
	
	print found	
	print c






def search_11():

	found = False
	c = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']

	retry = 10
	retry_bytes = chr(retry)

	fcp = '62 2F 87 01 08 83 02 00 20 80 02 00 10 8A 01 04 86 0E 00 FF C0 30 00 FF 00 10 00 FF 00 10 00 00 85 0F 00 01 00 00 AA 00 04 10 00 00 00 00 00 FF FF'
	fcp = fcp.split()
	fcp = ''.join(fcp)
	fcp_intarray = hexstring_to_intarray(fcp)
	fcp_bytes = intarray_to_asciiarray(fcp_intarray)

	# I have a feeling that I need the date
	# therefore must re run!

	for hash_name in [hs.sha1, hs.sha224, hs.sha256, hs.sha384, hs.sha512, hs.md5]:
		for hn in hs.algorithms_available:

			h1 = hs.new(hn)
			h1.update(str(intarray_to_hexstring(pin_list)))
			hashed_password = h1.digest()
			
			# xxx = X_list
			# for i in fcp_intarray:
			# 		xxx.append(i)
			# msg = ''.join(intarray_to_asciiarray(xxx))
			msg = X2.lower()

			dig = hmac.new(hashed_password, msg, hash_name)
			d = first_16_out(dig.hexdigest())
			d = hexstring_to_intarray(d)
			
			found = d == Y_list

			if found:
				print 'FOUND YA BASTARD HAHAHAHAHAHA!'
				print ''
				print Y_list
				print d
				print '--------------'
			elif d[0] == Y_list[0]:
				print 'something relevant'
				print ''
				print Y_list
				print Y_list_invert
				print d
				print '------------'
			c+=1
	
	print found	
	print c


search_11()
