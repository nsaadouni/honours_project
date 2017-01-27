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
					print 'METHOD FOUND'
					print 'padding is at the ' + padding_str[pad_index]
					print 'pad char (int): ' + str(i)
					print 'hash name: ' + str(hash_name)
					print 'rounds: ' + str(i)
					print ''
					print Y_list
					print out
					print '--------------'
				c+=1

	print found	
	print c



# _hashes = ['sha', 'sha1', 'sha256']# 'sha224', 'sha256', 'sha384', 'sha512', 'md4', 'md5', 'DSA-SHA', 'DSA', 'ecdsa-with-SHA1', 'ripemd160', 'whirlpool']
# p = Pool(3)
# p.map(search_2, _hashes)
