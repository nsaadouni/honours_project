from base import *
from multiprocessing import Pool
import itertools


"""
pbkdf2 -> password based key derivation function 2 (PKCS #5, RSA labortories created this)

"""
def search_2(hash_name):

	found = False
	c = 0

	for rounds in range(1,100001):
 
			# password -> ASCII
			password = []
			for i in intarray_to_asciiarray(pin_list):
				password.append(i)
			password = ''.join(password)
			
			# random number X -> ASCII
			salt = []
			for i in intarray_to_asciiarray(X_list)
			salt.append(i)
			salt = ''.join(salt)

			# password based key derviation function HMAC, truncated down to 16 bytes (First 16 only, as its the common practice)
			dk = hs.pbkdf2_hmac(hash_name, password, salt, rounds, 16)
			dkk = ba.hexlify(dk)
			t = hexstring_to_intarray(dkk)
			
			if t == Y_list:
				found = True

			if found:
				print 'METHOD FOUND'
				print 'hash name: ' + str(hash_name)
				print 'rounds: ' + str(i)
				print ''
				print Y_list
				print out
				print '--------------'
			c+=1

	print found	
	print c




hash_names = ['sha1', 'sha256', 'sha384', 'sha512', 'md5']
name = Pool(5)
name.map(search_2, hash_names)
