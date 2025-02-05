from base import *

"""
HMAC(password=pin, key=X, hash_name)

Also need to do 

HMAC(password=X, key=pin, hash_name)
"""
def search_10():

	found = False
	c = 0

	padding = [pad_end, pad_start]
	padding_str = ['END', 'START']
	
	outputs = [first_16_out, last_16_out, mod_out]
	str_outputs = ['first 16', 'last 16', 'mod out']


	for hash_name in [hs.sha1, hs.sha256, hs.sha384, hs.sha512, hs.md5]:

		
		key = ''.join(intarray_to_asciiarray(X_list))
		password = intarray_to_asciiarray(pin_list)

		dig = hmac.new(password, key, hash_name)
		d = out(dig.hexdigest())
		d = hexstring_to_intarray(d)
		
		found = d == Y_list

		if found:
			print 'METHOD FOUND'
			print 'output format: ' + str_outputs[out_index]
			print 'hash name: ' + str(hash_name)
			print Y_list
			print d
			print '--------------'
		c+=1

print found	
print c

search_10