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
	DATA -> everything except for last two hex digits

	SW1  -> 2nd two last two hex
	SW2  -> last two hex

"""

import sys

counter = 1

file_path = sys.argv[1]
file_name = file_path.split('/')[-1].split('.out')[0]
file_name += '.parsed'
parsed_output = open('./apdu_parsed_logs/' + file_name, 'w+')




for line in sys.stdin:

	s = '----- APDU command/response pair ' + str(counter) + ' -----'


	x = line.split()
	y = x[1:]
	if x[1] == 'APDU:':
		parsed_output.write(s + "\n")
		parsed_output.write('C ' + ' '.join(y[1:]) + "\n")
		#print s
		#print 'C ' + ' '.join(y[1:])
		counter +=1
	
	elif x[1] == 'SW:':
		parsed_output.write('R ' + ' '.join(y[1:]) + "\n\n")
		#print 'R ' + ' '.join(y[1:])
		#print ''