from base import *

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
								print 'METHOD FOUND'
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
								break
							c+=1
	
	print found	
	print c




search_1()