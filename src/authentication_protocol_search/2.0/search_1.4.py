from base import *
from Crypto.Cipher import AES

def search_4():

	found = False
	counter = 0

	# outputs = [first_16_out, last_16_out, mod_out]
	# str_outputs = ['first 16', 'last 16', 'mod out']

	for pad_index, pad in enumerate(padding):
		for i in range(256):

			hash_name = 'sha256'
			h = hs.new(hash_name)

			X = intarray_to_asciiarray(X_list)
			for j in X:
				h.update(j)

			pin_ascii = intarray_to_asciiarray(pin_list)

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
			counter+=1
	
	print found	
	print counter






search_4()
