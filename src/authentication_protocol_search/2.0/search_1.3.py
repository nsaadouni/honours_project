from base import *
import hmac






"""
HMAC(X, PIN, hash)
"""
def search_3a():

	found = False
	c = 0
	
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']

	for hash_name in [hs.sha1, hs.sha224, hs.sha256, hs.sha384, hs.sha512, hs.md5]:
		for out_index, out in enumerate(outputs):
			
			PIN = ''.join(intarray_to_asciiarray(pin_list))
			X = ''.join(intarray_to_asciiarray(X_list))
			dig = hmac.new(X, PIN, hash_name)

			d = out(dig.hexdigest())
			d = hexstring_to_intarray(d)
			

			if d == Y_list:
				found = True
				print 'METHOD FOUND'
				print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print d
				print '--------------'
			c+=1
	
	print found	
	print c



"""
HMAC(PIN, X, hash)
"""
def search_3b():

	found = False
	c = 0
	
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']

	for hash_name in [hs.sha1, hs.sha224, hs.sha256, hs.sha384, hs.sha512, hs.md5]:
		for out_index, out in enumerate(outputs):
			
			PIN = ''.join(intarray_to_asciiarray(pin_list))
			X = ''.join(intarray_to_asciiarray(X_list))
			dig = hmac.new(PIN, X, hash_name)

			d = out(dig.hexdigest())
			d = hexstring_to_intarray(d)
			

			if d == Y_list:
				found = True
				print 'METHOD FOUND'
				print 'output format: ' + str_outputs[out_index]
				print 'hash name: ' + str(hash_name)
				print ''
				print Y_list
				print d
				print '--------------'
			c+=1
	
	print found	
	print c



s
earch_3b()
search_3a()
