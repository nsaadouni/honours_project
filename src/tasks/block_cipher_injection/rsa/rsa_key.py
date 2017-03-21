# generate rsa 2044 bit key and save it in a file
# function LOAD_pub -> output N||E int array of bytes
# function decrypt_data -> load private key, decrypt int array (?), output int array of bytes

# MUST BE DONE IN THE MORNING AND THEN TEST IT OUT


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP

import binascii as ba
import sys

def hexstring_to_intarray(x):
    out = []
    # if len(x) % 2 != 0:
    #     x = '0' + x

    for i in range(0,len(x), 2):
        out.append(int((x[i]+x[i+1]),16))
        # ba.unhexlify(x[i]+x[i+1])
    return out

def generate_RSA(file_name, bits=1024, e=5):
    
    new_key = RSA.generate(bits, e=e)
    file = open('./' + file_name + '.der', 'w+')
    file.write(new_key.exportKey('DER'))
    file.close()


def load_key(file_name='rsa_2048.pem'):

	file = open(file_name,'r')
	key = RSA.importKey(file.read())

	public_key = key.publickey()
	private_key = key

	return public_key, private_key


def N_int_array(public_key):
	
    t = hexstring_to_intarray(hex(public_key.__getattr__('n'))[2:-1] + '6109')
    msg = str(t)
    for i in msg.split('[')[1].split(']')[0].split(','):
        sys.stdout.write(i.strip() +' ')

    print ''

def E_int_array(public_key):
    
    t = hexstring_to_intarray(hex(public_key.__getattr__('e'))[2:-1])
    msg = str(t)
    for i in msg.split('[')[1].split(']')[0].split(','):
        sys.stdout.write(i.strip() +' ')

    print ''


# decrypt int array response from card
def decrypt_response(response):
    return 0

#####################################################
#					Running Area					#
#####################################################

"""
Need to print in an intger array the public key that I created!
Only the public modulus is needed as the public exponent is the same on the card! (Done) -> N_int_array(public_key)

Need to be able to decrypt the response!
"""

# generate_RSA('rsa_2048', 2048)
# generate_RSA('rsa_1024', 1024)
# generate_RSA('_key', 1024, 65537)

public_key, private_key = load_key('rsa_2048.pem')
# _, private_key = load_key('_key.der')
# public_key = RSA.importKey('public_key.der')
t = hexstring_to_intarray(hex(public_key.__getattr__('n'))[2:-1])
print t
print ''

# file = open('./' + 'public_key' + '.der', 'w+')
# file.write(public_key.exportKey('DER'))
# file.close()

response_2048 = [140, 202, 117, 145, 252, 152, 222, 6, 224, 139, 172, 198, 168, 142, 12, 246, 196, 92, 129, 150, 142, 136, 127, 160, 44, 83, 28, 1, 50, 71, 173,
 240, 255, 199, 76, 242, 49, 159, 197, 238, 102, 41, 140, 110, 108, 146, 167, 89, 90, 31, 148, 131, 100, 152, 213, 21, 221, 166, 233, 55, 95, 242, 109, 17, 181, 56, 235, 40, 153,
  130, 65, 254, 101, 1, 237, 29, 96, 65, 148, 79, 107, 33, 240, 54, 78, 122, 20, 68, 171, 236, 228, 131, 186, 86, 213, 41, 52, 25, 109, 68, 156, 53, 99, 32, 196, 20, 17, 6, 71, 235, 
  57, 214, 21, 34, 89, 25, 116, 213, 236, 158, 156, 232, 30, 119, 195, 103, 140, 44]

response = [42, 5, 199, 247, 8, 134, 80, 166, 28, 111, 18, 119, 253, 165, 37, 240, 226, 78, 83, 87, 10, 16, 165, 
            250, 138, 179, 46, 93, 36, 218, 4, 114, 138, 37, 233, 79, 184, 65, 22, 11, 96, 237, 239, 175, 131, 228, 44, 160, 223, 147, 144, 105, 175, 155, 191,
             106, 79, 140, 179, 61, 191, 134, 17, 18, 236, 148, 108, 226, 94, 176, 85, 13, 157, 232, 41, 134, 83, 146, 251, 124, 97, 111, 149, 137, 247, 106, 224,
              232, 122, 41, 92, 156, 122, 44, 238, 228, 152, 125, 161, 69, 190, 90, 122, 215, 139, 221, 182, 69, 54, 143, 222, 254, 230, 167, 81, 213, 64, 2, 99, 38,
               17, 1, 0, 210, 105, 215, 166, 128]

ha = [163, 95, 38, 153, 44, 212, 141, 247, 186, 65, 159, 132, 187, 162, 10, 58, 27, 231, 76, 140, 194, 229, 147, 226, 157, 182, 246, 131, 228, 65, 35, 106, 82, 16, 114, 107, 1, 234, 0, 84, 1, 84, 224, 193, 181, 39, 3, 201, 94, 162, 184, 162, 96, 134, 247, 135, 1, 198, 177, 198, 24, 159, 137, 54, 79, 1, 61, 232, 193, 165, 145, 82, 180, 235, 23, 165, 238, 9, 74, 153, 205, 29, 249, 130, 50, 110, 97, 123, 159, 181, 186, 228, 61, 143, 92, 228, 89, 69, 210, 181, 2, 211, 15, 78, 145, 33, 15, 207, 213, 156, 126, 198, 142, 231, 159, 160, 45, 215, 232, 166, 160, 209, 61, 55, 127, 215, 28, 75]

r = []
for i in response:
    r.append(chr(i))

r = ''.join(r)

h = []
for i in ha:
    h.append(chr(i))
h = ''.join(h)

cipher = PKCS1_v1_5.new(public_key)
r = cipher.encrypt('nordine saadouni'+h[0:112])
print r
print len(r)
print ''
cipher = PKCS1_v1_5.new(private_key)
message = cipher.decrypt(r[0:128], h[0:112])

print message
print len(message)
print ba.hexlify(message)
print ''





# print private_key.decrypt(public_key.encrypt(msg, 'a'))

# N_int_array(public_key)
# print ''
# E_int_array(public_key)

for i in hexstring_to_intarray(ba.hexlify(message)):
    sys.stdout.write(str(i) + ' ')

print ''