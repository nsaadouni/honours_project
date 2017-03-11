#!/usr/bin/python

"""
This script takes in as input, the output of pcscd -a -f (APDU commands)

open file given as argument :) ----> can loop through them later if i want
grab file name (split(.out))
open new file call it file_name.parsed

if APDU COMMAND split into:
	CLA -> 1st two hex
	INS -> 2nd two hex
	P1  -> 3rd two hex 
	P2  -> 4th two hex

	Lc
	DATA
	Le

if APDU RESPONSE (SW) split into:
	DATA -> everything except for last four hex digits

	SW1  -> 2nd two last two hex
	SW2  -> last two hex

"""

import sys
import binascii as ba

file_path = sys.argv[1]
file_name = file_path.split('/')[-1].split('.out')[0]
file_name += '.py'
create_python_file = open('./' + file_name, 'w+')

def hexstring_to_intarray(x):
	x = ''.join(x)
	out = []
	for i in range(0,len(x), 2):
		# out.append(int((x[i]+x[i+1]),16))
		ba.unhexlify(x[i]+x[i+1])
	return out

def convert_to_intarray(x):

	out = []
	for i in x:
		out.append(int(i,16))
	return out



# create start of the python file
create_python_file.write('from smartcard.System import readers\n\n\n')
create_python_file.write('r = readers()\n')
create_python_file.write('print "Available readers:", r\n')
create_python_file.write('reader = r[-1]\n')
create_python_file.write('print "Using:", reader\n')
create_python_file.write('connection = reader.createConnection()\nconnection.connect()\n\n\n')


counter = 1


for line in sys.stdin:

	s = '----- APDU command/response pair ' + str(counter) + ' -----'

	x = line.split()
	if x[1] == 'APDU:':
		y = x[2:]
		

		command = str(convert_to_intarray(y))
		create_python_file.write('# APDU Command ' +  ' '.join(y) + '\n')
		create_python_file.write('command = ' + command + "\n")
		create_python_file.write('data, sw1, sw2 = connection.transmit(command)\n')
		create_python_file.write('print \'' + s + "\'\n")
		create_python_file.write('print \'C ' + ' '.join(y) + "\'\n")
		create_python_file.write('print \'R: %02X %02X\' % (sw1, sw2)\nprint data\nprint \'\'' + "\n\n\n")



		counter +=1
