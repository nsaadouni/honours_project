#!/usr/bin/python

"""
python script for locating the bus and device id of the
OmniKey AG CardMan 3121
"""

import sys

file_bus = open('bus.out', 'w+')
file_id = open('id.out', 'w+')

for line in sys.stdin:

	s = line.split()
	card_reader_name = 'OmniKey AG CardMan 3121'
	if ' '.join(s[-4:]) == card_reader_name:
		bus = int(s[1])
		file_bus.write(str(bus))
		file_id.write(s[3].split(':')[0])

file_id.close()
file_bus.close()