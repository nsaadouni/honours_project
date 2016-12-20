# from __future__ import division

# class Pin():

# 	def __init__(self, pin):
# 		self.pin = pin
# 		self.ascii_pin = self.pin_ascii_hex()


	# def pin_ascii_hex(self):
	# 	pin_hex = []
	# 	for i in self.pin:
	# 		pin_hex.append(str(int(i)+48))
	# 	return ''.join(pin_hex)


# 	#pad pin to make it 7 in length
# 	def pin_pad_end(self, pad=0):
# 		pin1 = []
# 		n = 7 - len(self.pin)
# 		pin1.append(self.ascii_pin)
# 		for i in range(n):
# 			pin1.append(str(pad))
# 		pin_1 = ''.join(pin1)
		
# 		return pin_1

	

# 	def pin_pad_start(self, pad=0):
# 		pin2 = []
# 		n = 7 - len(self.pin)
# 		for i in range(n):
# 			pin2.append(str(pad))
# 		pin2.append(self.ascii_pin)
# 		pin_2 = ''.join(pin2)

# 		return pin_2


# class RandomNumber():

# 	def __init__(self, x):
# 		self.X = ''.join(x.split())
# 		self.X07 = ''.join(x.split()[0:7])
# 		self.X18 = ''.join(x.split()[1:8])


# class Oracle():

# 	def __init__(self, out):
# 		self.out = ''.join(out.split())

###########################################################
# search method 1 complete 
	# Not found!
	# def search(self, printt=True):

	# 	found = False

	# 	joins = [self.join_1,self.join_2,self.join_3,self.join_4,self.join_5, self.join_6, self.join_7]
	# 	str_joins = ['join 1', 'join 2', 'join 3', 'join 4', 'join 5', 'join_6', 'join_7']

	# 	out_format = [self.standard_out, self.first_16_out, self.last_16_out, self.mod_out]
	# 	str_out = ['standard', 'first 16', 'last 16', 'mod 2^(8*16)']

	# 	str_joined_format = ['integer', 'hexidecimal']
	# 	str_pin_format = ['ascii pin', 'ascii pin padded start 48', 'ascii pin padded end 48','ascii pin padded start 00', 'ascii pin padded end 00']		

	# 	counter1 = 0
	# 	for f in joins:
	# 		X = int(self.X,16)

	# 		counter2 = 0
	# 		for pin in [self.ascii_pin, self.pin_pad_start(), self.pin_pad_end(),self.pin_pad_start('00'), self.pin_pad_end('00')]:
	# 			pin = int(pin,16)
				
	# 			# integer format
	# 			joined_integer =  str(f(pin,X))

	# 			# hex format
	# 			joined_hex = hex(f(pin,X))[2:]

	# 			counter3 = 0
	# 			for output_format in out_format:
					
	# 				counter4 = 0
	# 				for joined_format in [joined_integer, joined_hex]:

	# 					for hash_used in hs.algorithms_available:

	# 						h = hs.new(hash_used)
	# 						h.update(joined_format)
	# 						calc = h.hexdigest()

	# 						calc_Y = output_format(calc)
	# 						if calc_Y[-1] == 'L':
	# 							calc_Y = calc_Y[0:-1]

	# 						if printt:
	# 							print 'hash function used: ' + str(hash_used)
	# 							print 'join used: ' + str_joins[counter1]
	# 							print 'pin format: ' + str_pin_format[counter2]
	# 							print 'output format: ' + str_out[counter3]
	# 							print 'hex or int: ' + str_joined_format[counter4]
	# 							print calc_Y
	# 							#print self.Y
	# 							print calc_Y == self.Y
	# 							print '--------------'

	# 						if calc_Y == self.Y:
	# 							found = True
						
	# 					counter4 += 1
	# 				counter4=0
	# 				counter3+=1
	# 			counter3=0
	# 			counter2+=1
	# 		counter2=0
	# 		counter1+=1
	# 	counter1=0


	# 	print 'Found method -> ' + str(found)
################################################################################################
import hashlib as hs
"""
ascii
Decimal		| Hex 		| Oct
	48(0)		30			60
	49(1)		31			61
	50(2)		32			62
	51(3)		33			63
	52(4)		34			64
	53(5)		35			65
	54(6)		36			66
	55(7)		37			67
	56(8)		38			70
	57(9)		39			71
"""
class find_method():

	def __init__(self, pin, X, Y):

		self.pin = pin
		self.hex_pin = self.pin_hex()
		self.ascii_pin_hex = self.pin_ascii_hex()
		self.ascii_pin_dec = self.pin_ascii_dec()
		
		self.ran = X
		self.X = ''.join(X.split())
		self.X06 = ''.join(X.split()[0:7])
		self.X17 = ''.join(X.split()[1:8])
		self.X0 = ''.join(X.split()[0])
		self.X7 = ''.join(X.split()[7])


		self.Y = hex(int(''.join(Y.split()),16))[2:-1]


	def print_attributes(self):
		print self.pin
		print self.pin_pad_start()
		print self.pin_pad_end()
		print '----------------'
		print self.X
		print '----------------'
		print self.Y
		print '----------------'

	
	def pin_hex(self):
		pin_hex = []
		for i in self.pin:
			pin_hex.append('0')
			pin_hex.append(str(i))
		return ''.join(pin_hex)

	def pin_ascii_hex(self):
		pin_ascii_hex = []
		for i in self.pin:
			pin_ascii_hex.append(str(int(i)+30))
		return ''.join(pin_ascii_hex)

	def pin_ascii_dec(self):
		pin_ascii_dec = []
		for i in self.pin:
			pin_ascii_dec.append(str(int(i)+48))
		return ''.join(pin_ascii_dec)

######################################################################

	def pin_pad_end(self, pin, padd='00'):
		pad = []
		if len(padd) < 2:
			pad.append('0')

		pad.append(padd)
		pad = ''.join(pad)

		pin1 = []
		n = 7 - len(self.pin)
		pin1.append(pin)
		for i in range(n):
			pin1.append(str(pad))
		pin_1 = ''.join(pin1)
		return pin_1

	def pin_pad_start(self, pin, padd='00'):
		pad = []
		if len(padd) < 2:
			pad.append('0')

		pad.append(padd)
		pad = ''.join(pad)

		pin2 = []
		n = 7 - len(self.pin)
		for i in range(n):
			pin2.append(str(pad))
		pin2.append(pin)
		pin_2 = ''.join(pin2)
		return pin_2

######################################################################


	def join_1(self,pin, X):
		out = X ^ pin
		return out

	def join_2(self,pin,X):
		out = X+pin
		return out

	def join_3(self, pin,X):
		out = X*pin
		return out

	def join_4(self,pin,X):
		out = ((X-pin)**2)**(1/2)
		return out

	def join_5(self, pin,X):
		#concatination start
		# INPUT IS IN BASE 10 !! NEED TO CONVERT BACK TO 16!
		pin = hex(pin)[2:]
		X = hex(X)[2:]
		if pin[-1] == 'L':
			pin = pin[0:-1]
		if X[-1] == 'L':
			X = X[0:-1]
		out = []
		out.append(str(pin))
		out.append(str(X))
		return int(''.join(out),16)

	def join_6(self, pin,X):
		#concatination end
		# INPUT IS IN BASE 10 !! NEED TO CONVERT BACK TO 16!
		pin = hex(pin)[2:]
		X = hex(X)[2:]
		if pin[-1] == 'L':
			pin = pin[0:-1]
		if X[-1] == 'L':
			X = X[0:-1]
		out = []
		out.append(str(pin))
		out.append(str(X))
		return int(''.join(out),16)

	def join_7(self, pin,X):
		# concatination mixed (start) [only for search 2]
		# INPUT IS IN BASE 10 !! NEED TO CONVERT BACK TO 16!
		pin = hex(pin)[2:]
		X = hex(X)[2:]
		if pin[-1] == 'L':
			pin = pin[0:-1]
		if X[-1] == 'L':
			X = X[0:-1]

		out = []
		for i in range(len(pin)):
			out.append(X[i])
			out.append(pin[i])

		return int(''.join(out),16)

	def join_8(self, pin,X):
		#concatination mixed (end) [only for search 2]
		# INPUT IS IN BASE 10 !! NEED TO CONVERT BACK TO 16!
		pin = hex(pin)[2:]
		X = hex(X)[2:]
		if pin[-1] == 'L':
			pin = pin[0:-1]
		if X[-1] == 'L':
			X = X[0:-1]

		out = []
		for i in range(len(pin)):
			out.append(pin[i])
			out.append(X[i])

		return int(''.join(out),16)


######################################################################

	def standard_out(self, calc_Y):
		return calc_Y

	def first_16_out(self, calc_Y):
		return calc_Y[0:32]

	def last_16_out(self, calc_Y):
		return calc_Y[-33:-1]
	
	def mod_out(self, calc_Y):
		out = int(calc_Y,16)
		out = out % (2**(8*16))
		return hex(out)[2:]

######################################################################in

	# ISSUE THAT I AM NOT FIXING -> STATDARD PIN GETS PADDING OF DOUBLE 00'S AS WELL INSTEAD OF 1
	def search_1(self, printt=False):
		found = False

		pins = [self.hex_pin, self.ascii_pin_hex, self.ascii_pin_dec]
		str_pins = ['standard pin in hex', 'pin assci hex', 'pin ascii decimal']

		# join 5 is no good
		joins = [self.join_1,self.join_2,self.join_3,self.join_4,self.join_5, self.join_6]
		str_joins = ['join 1', 'join 2', 'join 3', 'join 4', 'join 5', 'join 6']

		format_output = [self.standard_out, self.first_16_out, self.last_16_out, self.mod_out]
		str_format_output = ['standard', 'first 16', 'last 16', 'mod 2^(8*16)']

		str_input_to_hash = ['joined integer', 'joined hexideciaml', 'joined ascii from int', 'joined ascii from hex', 'joined_binary']

		X = int(self.X,16)

		# select pin type
		for pi, p in enumerate(pins):
			# pad pin wth all possibilites
			for i in range(-256,256):
				
				# no padding used when 00 at start so this is fine				
				if i < 0:
					# pad pin at start
					pin = self.pin_pad_start(p, str(hex((i*-1)-1)[2:]))
					padding = 'pin padded at start with: ' + str(hex((i*-1)-1)[2:])
				else:
					# pad pin at end
					pin = self.pin_pad_end(p, str(hex(i)[2:]))
					padding = 'pin padded at end with: ' + str(hex(i)[2:])

				# convert to base 10
				pin = int(pin,16)

				# join the pin and the random number
				for ji, j in enumerate(joins):

					# integer format
					joined_integer =  str(j(pin,X))

					# hex format
					joined_hex = hex(j(pin,X))[2:]
					if joined_hex[-1] == 'L':
						joined_hex = joined_hex[0:-1]

					# ascii format form integer string
					joined_ascii_int = []
					for i in joined_integer:
						j = int(i)
						joined_ascii_int.append(chr(j))
					joined_ascii_int = ''.join(joined_ascii_int)

					# ascii format from hex string
					joined_ascii_hex = []
					for i in joined_hex:
						j = int(i,16)
						joined_ascii_hex.append(chr(j))
					joined_ascii_hex = ''.join(joined_ascii_hex)

					# binary format of number
					joined_binary = bin(int(joined_integer))[2:]


					input_format_to_hash = [joined_integer, joined_hex, joined_ascii_int, joined_ascii_hex, joined_binary]


					# try all input formats to hash functons
					for hii, hi in enumerate(input_format_to_hash):

						# select how the output should be formatted
						for outi, out in enumerate(format_output):

							for hash_used in hs.algorithms_available:

								h = hs.new(hash_used)
								h.update(hi)
								calc = h.hexdigest()

								calc_Y = out(calc)
								if calc_Y[-1] == 'L':
									calc_Y = calc_Y[0:-1]


								if printt:
									print 'pin type used: ' + str_pins[int(pi)]
									print padding
									print 'join function: ' + str_joins[int(ji)]
									print 'input format to hash: ' + str_input_to_hash[int(hii)]
									print 'output format: ' + str_format_output[int(outi)]
									print 'hash function used: ' + str(hash_used)
									print calc_Y
									#print self.Y
									print calc_Y == self.Y
									print '--------------'

								if calc_Y == self.Y:
									found = True
									print 'pin type used: ' + str_pins[pi]
									print padding
									print 'join function: ' + str_joins[ji]
									print 'input format to hash: ' + str_input_to_hash[hi]
									print 'output format: ' + str_format_output[outi]
									print 'hash function used: ' + str(hash_used)
									print calc_Y
									#print self.Y
									print calc_Y == self.Y
									print '--------------'

		print 'Found method -> ' + str(found)




	# X is the first 7 elements of the random number
	# Try hashing the 8th element and joining it to join(pin,X)
	def search_2(self, printt=False, first=True):
		found = False

		pins = [self.hex_pin, self.ascii_pin_hex, self.ascii_pin_dec]
		str_pins = ['standard pin in hex', 'pin assci hex', 'pin ascii decimal']

		# join 5 is no good
		joins = [self.join_1,self.join_2,self.join_3,self.join_4,self.join_5, self.join_6, self.join_7, self.join_8]
		str_joins = ['join 1', 'join 2', 'join 3', 'join 4', 'join 5', 'join 6']

		format_output = [self.standard_out, self.first_16_out, self.last_16_out, self.mod_out]
		str_format_output = ['standard', 'first 16', 'last 16', 'mod 2^(8*16)']

		str_input_to_hash = ['joined integer', 'joined hexideciaml', 'joined ascii from int', 'joined ascii from hex', 'joined_binary']

		if first:
			X = int(self.X06,16)
		else:
			X = int(self.X17,16)

		# select pin type
		for pi, p in enumerate(pins):
			# pad pin wth all possibilites
			for i in range(-256,256):
				
				# no padding used when 00 at start so this is fine				
				if i < 0:
					# pad pin at start
					pin = self.pin_pad_start(p, str(hex((i*-1)-1)[2:]))
					padding = 'pin padded at start with: ' + str(hex((i*-1)-1)[2:])
				else:
					# pad pin at end
					pin = self.pin_pad_end(p, str(hex(i)[2:]))
					padding = 'pin padded at end with: ' + str(hex(i)[2:])

				# convert to base 10
				pin = int(pin,16)

				# join the pin and the random number
				for ji, j in enumerate(joins):

					# integer format
					joined_integer =  str(j(pin,X))

					# hex format
					joined_hex = hex(j(pin,X))[2:]
					if joined_hex[-1] == 'L':
						joined_hex = joined_hex[0:-1]

					# ascii format form integer string
					joined_ascii_int = []
					for i in joined_integer:
						j = int(i)
						joined_ascii_int.append(chr(j))
					joined_ascii_int = ''.join(joined_ascii_int)

					# ascii format from hex string
					joined_ascii_hex = []
					for i in joined_hex:
						j = int(i,16)
						joined_ascii_hex.append(chr(j))
					joined_ascii_hex = ''.join(joined_ascii_hex)

					# binary format of number
					joined_binary = bin(int(joined_integer))[2:]


					input_format_to_hash = [joined_integer, joined_hex, joined_ascii_int, joined_ascii_hex, joined_binary]


					# try all input formats to hash functons
					for hii, hi in enumerate(input_format_to_hash):

						# select how the output should be formatted
						for outi, out in enumerate(format_output):

							for hash_used in hs.algorithms_available:

								for method in range(2):

									h = hs.new(hash_used)
									addhii=0
									if hii == 0:
										addhii = int(hi)
										print hi

									if first:
										b = self.X7
									else:
										b = self.X0

									if method == 0:
										h.update(hi)
										calc = h.hexdigest()
										# need to join b (just add for now)
										calc = int(calc,16)
										calc *= int(b,16) # this is the join here
										calc = hex(calc)[2:]
										if calc[-1] == 'L':
											calc = calc[0:-1]
									
									elif method == 1:
										h.update(b)
										calc = h.hexdigest()
										# need to join hii (just add for now)
										calc = int(calc,16)
										calc *= addhii # this is the join here
										calc = hex(calc)[2:]
										print calc
										if calc[-1] == 'L':
											calc = calc[0:-1]

									calc_Y = out(calc)
									if calc_Y[-1] == 'L':
										calc_Y = calc_Y[0:-1]


									if printt:
										print 'pin type used: ' + str_pins[int(pi)]
										print padding
										print 'join function: ' + str_joins[int(ji)]
										print 'input format to hash: ' + str_input_to_hash[int(hii)]
										print 'output format: ' + str_format_output[int(outi)]
										print 'hash function used: ' + str(hash_used)
										print calc_Y
										#print self.Y
										print calc_Y == self.Y
										print '--------------'

									if calc_Y == self.Y:
										found = True
										print 'pin type used: ' + str_pins[pi]
										print padding
										print 'join function: ' + str_joins[ji]
										print 'input format to hash: ' + str_input_to_hash[hi]
										print 'output format: ' + str_format_output[outi]
										print 'hash function used: ' + str(hash_used)
										print calc_Y
										#print self.Y
										print calc_Y == self.Y
										print '--------------'

		print 'Found method -> ' + str(found)
		print self.Y



	def print_attributes(self):
		print 'pin: ' + str(self.pin)
		print 'hex pin: ' + str(self.hex_pin)
		print 'ascii pin hex: ' + str(self.ascii_pin_hex)
		print 'ascii pin dec: ' + str(self.ascii_pin_dec)
		print ''
		print 'random number: ' + str(self.ran)
		print 'X: ' + str(self.X)
		print 'first 7 elemts of X: ' + str(self.X06)
		print 'last 7 elements of X: ' + str(self.X17)
		print ''
		print 'Y: ' + str(self.Y)










pin = '12345'
X ='29 C7 29 1F ED 13 23 7B'
Y = 'AE 69 B8 4B 7D BE BB 2B 63 63 D3 7D 07 9D D3 EC'

search = find_method(pin, X, Y)
search.search_1()
search.search_2(first=True)
search.search_2(first=False)
# search.print_attributes()






