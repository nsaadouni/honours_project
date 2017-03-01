from base import *


"""
AES-CBC(key=pin, IV=sha256(X)[16:32], msg=sha256(X)[0:15])

No
"""

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
