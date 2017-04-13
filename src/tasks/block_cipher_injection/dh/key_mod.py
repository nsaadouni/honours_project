
import sys

start = [128, 1, 0]

control_2 = [129, 129, 128]
key_1 = [247, 181, 21, 114, 7, 34, 148, 111, 196, 8, 100, 203, 189, 175, 234, 85, 125, 189, 143, 85, 54, 176, 1, 194, 139, 46, 50,
 182, 93, 69, 241, 116, 93, 56, 18, 11, 173, 157, 44, 3, 156, 34, 70, 104, 235, 46, 162, 140, 32, 149, 168, 46, 108, 168, 224, 109, 71, 242, 211, 30,
  215, 1, 248, 21, 92, 173, 220, 5, 112, 192, 147, 178, 109, 116, 176, 155, 149, 230, 77, 140, 210, 252, 115, 62, 205, 15, 48, 104, 121, 165, 185,
   53, 242, 65, 63, 82, 173, 173, 50, 160, 153, 26, 24, 61, 204, 87, 126, 57, 218, 71, 83, 30, 103, 21, 171, 1, 112, 127, 242, 71, 150, 113, 68,
    35, 206, 123, 96, 103]

control_3 = [130, 129, 128]
key_2 = [60, 82, 210, 6, 137, 40, 146, 44, 171, 230, 60,
 		 78, 230, 223, 14, 210, 41, 241, 1, 190, 54, 196, 248, 84, 64, 86, 243, 74, 250, 141, 46, 155, 96, 245, 7, 188, 237,
 		 180, 68, 86, 104, 93, 130, 76, 196, 234, 215, 150, 32, 248, 197, 70, 166, 224, 22, 184, 171, 165, 216, 67, 41, 88,
 		 83, 119, 23, 9, 151, 170, 112, 104, 51, 158, 241, 65, 10, 95, 57, 217, 117, 36, 127, 58, 83, 99, 97, 71, 135, 135,
 		 127, 136, 150, 188, 187, 131, 161, 203, 209, 66, 224, 235, 153, 207, 52, 14, 202, 86, 79, 44, 87, 80, 110, 123, 26,
 		 252, 31, 144, 122, 224, 194]

cert_2 = [168, 93, 211, 48, 227, 92, 169, 0, 57]


# 61 09 (9 more bytes to come)
SW_1 = [97, 9]
# 90 00 complete successfully
SW_2 = [144, 0]



###########################################################
#					Running Area						  #
###########################################################


def print_ints(command):

	for i in command:
		sys.stdout.write( str(i) +' ')
	print '\n'



command1 = []
command11 = []

for i in start:
	command1.append(i)

for i in control_2:
	command1.append(i)

for i in key_1:
	command1.append(0)

for i in control_3:
	command1.append(i)

for i in key_2:
	command1.append(i)

for i in SW_1:
	command1.append(i)

for i in cert_2:
	command11.append(i)

for i in SW_2:
	command11.append(i)

# print_ints(command1)
# print_ints(command11)

print ''


print ''
# print len(command1)
print '\n-------------------\n\n'

command1 = []
command11 = []

for i in start:
	command1.append(i)

for i in control_2:
	command1.append(i)

for i in key_1:
	command1.append(i)

for i in control_3:
	command1.append(i)

# command1.append(1)

for i in range(119):
	command1.append(0)

for i in SW_1:
	command1.append(i)

for i in range(9):
	command11.append(0)

for i in SW_2:
	command11.append(i)

print_ints(command1)
print_ints(command11)




print '\n------------------------------\n\n\n'



# x1 = 'C8 04 C7 25 A9 14 2D 58  E8 01 64 6D 72 DA C4 9C' 
x1 = 'FA AD 82 BB C2 95 69 6E  2C 69 DF B2 75 90 DF BD'

x2 = 'A5 F0 D1 FA AF 53 93 A7  49 8D 69 8B 7A 1A D0 A4' 
x3 = '90 00'

xx = []
for i in x1.split():
	xx.append(int(i,16))
	# xx.append(0)

for i in x2.split():
	# xx.append(int(i,16))
	xx.append(0)

for i in x3.split():
	xx.append(int(i,16))
	# xx.append(0)



# print_ints(xx)

