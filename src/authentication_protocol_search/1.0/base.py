import math
import hashlib as hs 
import binascii as ba


######################################################

# input: array of characters (string)
# output: array of integers
def asciiarray_to_intarray(x):

	out = []
	for i in x:
		out.append(ord(i))
	return out

# input: array of integers
# output: array of ascii characters
def intarray_to_asciiarray(x):

	out = []
	for i in x:
		out.append(chr(i))
	return out

# input: array of integers
# output: string of hexidecimals
def intarray_to_hexstring(x):
	out = []
	for i in x:

		if i < 16:
			out.append('0'+hex(i)[2:])
		else:
			out.append(hex(i)[2:])

	# if out[-1] == 'L':
	# 	out = out[0:-1]
	return ''.join(out)

def hexstring_to_intarray(x):
	out = []
	if len(x) % 2 != 0:
		x = '0' + x

	for i in range(0,len(x), 2):
		out.append(int((x[i]+x[i+1]),16))
		# ba.unhexlify(x[i]+x[i+1])
	return out

def invert_intarray(x):
	out = []
	for i in x:
		out.append((~i) & 255)

	return out
#########################################################

# needs generalized to allow smaller and larger pins
# MIGHT JUST GET RID OF THIS!

def pad_end(pin, pad=255):
	out = []
	n = 16 - len(pin)
	for i in pin:
		out.append(i)
	for i in range(n):
		out.append(pad)

	return out

def pad_start(pin,pad=255):
	out = []
	n = 16 - len(pin)
	for i in range(n):
		out.append(pad)
	for i in pin:
		out.append(i)
	
	return out

def do_not_pad(pin, pad=255):
	return pin
##########################################################

def xor_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] ^ x_array[i])

 	return out

def nxor_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(~(pin_array[i] ^ x_array[i]) & 255)

 	return out

def or_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] | x_array[i])

 	return out

def nor_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append( (~(pin_array[i] | x_array[i])) & 255)

 	return out

def and_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(pin_array[i] & x_array[i])

 	return out


def nand_join(pin_array, x_array):
 	out = []
 	for i in range(len(pin_array)):
 		out.append(~(pin_array[i] & x_array[i]) & 255)

 	return out


################################################################

def first_16_out(hexdigest):
	return hexdigest[:32]

def last_16_out(hexdigest):
	return hexdigest[-32:]

def mod_out(hexdigest):
	out = int(hexdigest,16)
	out = out % (2**(8*16))
	out = hex(out)[2:]
	if out[-1] == 'L':
		out = out[0:-1]

	if len(out) < 32:
		return '0' + out
	else:
		return out








#########################################################
#				Running Area							#
#########################################################
# ascii
pin = '0000000000000000'
# hex
# X ='29 C7 29 1F ED 13 23 7B'
X = '68 F1 E4 92 85 36 39 A3'
# hex
# Y = 'AE 69 B8 4B 7D BE BB 2B 63 63 D3 7D 07 9D D3 EC'
Y  = '53 17 55 20 F4 30 18 56 80 E6 75 55 E1 91 A7 EC'

# pre process inputs into lists
pin_list = []
for i in pin:
	pin_list.append(ord(i))

pin_int = intarray_to_hexstring(pin_list)
pin_int = int(pin_int,16)

X_list = []
for i in X.split():
	X_list.append(int(i,16))

X2 = ''.join(X.split())
X_int = int(X2,16)

Y_list = []
for i in Y.split():
	Y_list.append(int(i,16))

Y_list_invert = invert_intarray(Y_list)


Y2 = ''.join(Y.split())
Y_int = int(Y2,16)
# Y2 = hex(Y2)[2:-1]

print ''
print 'pin: ' + pin
print 'pin list: ' + str(pin_list)
print 'pin list hex: ' + str(intarray_to_hexstring(pin_list))
print 'pin int: ' + str(pin_int)
print '--------------------------------------------'
print 'X: ' + X
print 'X2: ' + str(X2)
print 'X list: ' + str(X_list)
print 'X int: ' + str(X_int) 
print '--------------------------------------------'
print 'Y: ' + Y
print 'Y2: ' + Y2
print 'Y list: ' + str(Y_list)
print 'Y list inverted: ' + str(Y_list_invert)
print 'Y int: ' + str(Y_int)
print '--------------------------------------------'
print ''
