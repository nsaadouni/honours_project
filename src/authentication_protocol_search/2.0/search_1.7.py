from base import *



"""
AES-CMAC(key=pin, msg=X||X)

No
"""

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
