import math
import hashlib as hs
from bitarray import bitarray


"""
consider removing ascii hex decimal from normal shite
have a search method or itself as it doesnt quite make sense to convert that to integet via base 16! it is already base 10 but with a base 16 padding (WRONG)
"""

pin = 0x3132333435ffffff
x =   0x29C7291FED13237b
xpin = 0x29C7291FED13237b3132333435000000
y =    0xae69b84b7dbebb2b6363d37d079dd3ec

xx = 0x8BA2790FC9DDE8F6
yy = 0x4A3347768812D6ACAD2B2E43EFD77B48
# print pin
# print x 
# print y
# print pin * x
# print ''

# print y/x
# print yy/xx





for hu in hs.algorithms_available:
	h = hs.new(hu)
	test = []
	# print '0'+bin(pin^x)[2:]
	for i in hex(x^pin)[2:]:
		j = int(i,16)
		test.append(chr(j))
	# print test
	test = ''.join(test)

	h.update(test)
	print (int(h.hexdigest(),16))
	# print (int(h.hexdigest(),16))
	print (int(h.hexdigest(),16) % 2**(8*16))
	print y
	print '-----------------------'
	

# print bin(y)[2:]
# print bin(x)[2:]
# print bin(pin)[2:]
# print bin(x ^ pin)[2:]
# print bool(bin(pin)[6])

# bpin = bitarray(bin(pin)[2:])
# bx = bitarray(bin(x)[2:])

# print bpin
# print bx
# print (bpin ^ bx)
# print bin(pin^x)[2:]

# print bin(0x31)
# print bin(0x29)
# print bin((0x31 ^ 0x29) * 0x7b)
# print bin(0xae69)
# print hs.algorithms_available
h = hs.new('SHA256')
h.update(bin(pin^x)[2:])
print len(h.hexdigest())

# final push
"""
binary format -> bytes using chr(0) or chr(1)

hash that
compare
"""