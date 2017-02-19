from base import *
from multiprocessing import Pool
import itertools


"""
pbkdf2 -> password based key derivation function 2 (PKCS #5, RSA labortories created this)

"""
def search_2(hash_name):

	found = False
	c = 0

	for rounds in range(1,50001):
 
			# password -> ASCII
			password = []
			for i in intarray_to_asciiarray(pin_list):
				password.append(i)
			password = ''.join(password)
			
			# random number X -> ASCII
			salt = []
			for i in intarray_to_asciiarray(X_list)
:p				salt.append(i)
			salt = ''.join(salt)

			# password based key derviation function HMAC, truncated down to 16 bytes (First 16 only, as its the common practice)
			dk = hs.pbkdf2_hmac(hash_name, password, salt, rounds, 16)
			dkk = ba.hexlify(dk)
			t = hexstring_to_intarray(dkk)
			
			if t == Y_list:
				found = True

			if found:
				print 'METHOD FOUND'
				# print 'padding is at the ' + padding_str[pad_index]
				# print 'pad char (int): ' + str(i)
				print 'hash name: ' + str(hash_name)
				print 'rounds: ' + str(i)
				print ''
				print Y_list
				print out
				print '--------------'
			c+=1

	print found	
	print c





_hashes = ['sha', 'sha1', 'sha256']# 'sha224', 'sha256', 'sha384', 'sha512', 'md4', 'md5', 'DSA-SHA', 'DSA', 'ecdsa-with-SHA1', 'ripemd160', 'whirlpool']
name = Pool(2)
name.map(search_2, _hashes)
