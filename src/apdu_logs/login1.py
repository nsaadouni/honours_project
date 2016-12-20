from smartcard.System import readers


r = readers()
print "Available readers:", r
reader = r[-1]
print "Using:", reader
connection = reader.createConnection()
connection.connect()


# # APDU Command 00 A4 04 00 0C A0 00 00 01 64 4C 41 53 45 52 00 01 00
# command = [0, 164, 4, 0, 12, 160, 0, 0, 1, 100, 76, 65, 83, 69, 82, 0, 1, 0]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 1 -----'
# print 'C 00 A4 04 00 0C A0 00 00 01 64 4C 41 53 45 52 00 01 00'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 80 A4 08 00 06 3F 00 30 00 EE EE
# command = [128, 164, 8, 0, 6, 63, 0, 48, 0, 238, 238]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 2 -----'
# print 'C 80 A4 08 00 06 3F 00 30 00 EE EE'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 00 B0 00 00 00
# command = [0, 176, 0, 0, 0]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 3 -----'
# print 'C 00 B0 00 00 00'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 80 A4 08 00 06 3F 00 30 00 C0 00
# command = [128, 164, 8, 0, 6, 63, 0, 48, 0, 192, 0]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 4 -----'
# print 'C 80 A4 08 00 06 3F 00 30 00 C0 00'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 00 B0 00 00 00
# command = [0, 176, 0, 0, 0]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 5 -----'
# print 'C 00 B0 00 00 00'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 80 A4 08 00 06 3F 00 30 00 30 04
# command = [128, 164, 8, 0, 6, 63, 0, 48, 0, 48, 4]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 6 -----'
# print 'C 80 A4 08 00 06 3F 00 30 00 30 04'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 80 A4 08 00 08 3F 00 30 00 30 01 D0 7E
# command = [128, 164, 8, 0, 8, 63, 0, 48, 0, 48, 1, 208, 126]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 7 -----'
# print 'C 80 A4 08 00 08 3F 00 30 00 30 01 D0 7E'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 80 A4 08 00 08 3F 00 30 00 30 03 40 00
# command = [128, 164, 8, 0, 8, 63, 0, 48, 0, 48, 3, 64, 0]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 8 -----'
# print 'C 80 A4 08 00 08 3F 00 30 00 30 03 40 00'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Command 00 B0 00 02 64
# command = [0, 176, 0, 2, 100]
# data, sw1, sw2 = connection.transmit(command)
# print '----- APDU command/response pair 9 -----'
# print 'C 00 B0 00 02 64'
# print 'R: %02X %02X' % (sw1, sw2)
# print data
# print ''


# # APDU Cpyth


# APDU Command 80 A4 08 00 04 3F 00 00 20
command = [128, 164, 8, 0, 4, 63, 0, 0, 32]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 11 -----'
print 'C 80 A4 08 00 04 3F 00 00 20'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 00 84 00 00 08
command = [0, 132, 0, 0, 8]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 12 -----'
print 'C 00 84 00 00 08'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 80 20 00 00 10 AE 69 B8 4B 7D BE BB 2B 63 63 D3 7D 07 9D D3 EC
command = [128, 32, 0, 0, 16, 174, 105, 184, 75, 125, 190, 187, 43, 99, 99, 211, 125, 7, 157, 211, 236]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 13 -----'
print 'C 80 20 00 00 10 AE 69 B8 4B 7D BE BB 2B 63 63 D3 7D 07 9D D3 EC'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 80 A4 08 00 08 3F 00 30 00 30 03 40 01
command = [128, 164, 8, 0, 8, 63, 0, 48, 0, 48, 3, 64, 1]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 14 -----'
print 'C 80 A4 08 00 08 3F 00 30 00 30 03 40 01'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 00 B0 00 03 01
command = [0, 176, 0, 3, 1]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 15 -----'
print 'C 00 B0 00 03 01'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 80 A4 08 00 08 3F 00 30 00 30 02 D0 7E
command = [128, 164, 8, 0, 8, 63, 0, 48, 0, 48, 2, 208, 126]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 16 -----'
print 'C 80 A4 08 00 08 3F 00 30 00 30 02 D0 7E'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 80 A4 08 00 08 3F 00 30 00 30 01 D0 7E
command = [128, 164, 8, 0, 8, 63, 0, 48, 0, 48, 1, 208, 126]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 17 -----'
print 'C 80 A4 08 00 08 3F 00 30 00 30 01 D0 7E'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 80 A4 08 00 06 3F 00 30 00 EE EF
command = [128, 164, 8, 0, 6, 63, 0, 48, 0, 238, 239]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 18 -----'
print 'C 80 A4 08 00 06 3F 00 30 00 EE EF'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 00 B0 00 00 00
command = [0, 176, 0, 0, 0]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 19 -----'
print 'C 00 B0 00 00 00'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


# APDU Command 80 28 00 00 04 00 00 00 20
command = [128, 40, 0, 0, 4, 0, 0, 0, 32]
data, sw1, sw2 = connection.transmit(command)
print '----- APDU command/response pair 20 -----'
print 'C 80 28 00 00 04 00 00 00 20'
print 'R: %02X %02X' % (sw1, sw2)
print data
print ''


