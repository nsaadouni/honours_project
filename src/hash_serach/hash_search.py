#!/usr/bin/python

import hashlib as hb 

def print_all_hashes():
	for x in hb.algorithms_available:
		print(x)


#print('The list of hash\'s I will test are here')
#print_all_hashes()


# uses 
def find_hash_used(x, y):

	found = False
	for hash in hb.algorithms_available:
		h = hb.new(hash)
		h.update(x)
		s = h.hexdigest()
		yy = int(s,16)
		if y == yy:
			print('hash found: ')
			print(hash)
			found = True

	if found == False:
		print('hash not found')




# whirlpool hash for string:
#	'This is a test string to be used in explanation'

x = 'This is a test string to be used in explanation'
y = int('1a22fb7cca7be8088333d7a656ff4d10887184ff7aa4184594d6970938efabe3bced5f82d184360fee173ff890b8c72ff149825616f49f2ebad08ed0b450365b',16) 
find_hash_used(x,y)

# It works, now just to find out how to extract data from card! using pcsc-lite