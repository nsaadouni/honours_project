from base import *


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

#search_10