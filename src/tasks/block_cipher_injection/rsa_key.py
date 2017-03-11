# generate rsa 2044 bit key and save it in a file
# function LOAD_pub -> output N||E int array of bytes
# function decrypt_data -> load private key, decrypt int array (?), output int array of bytes

# MUST BE DONE IN THE MORNING AND THEN TEST IT OUT


from Crypto.PublicKey import RSA 
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

def generate_RSA(file_name, bits=2048):
    
    new_key = RSA.generate(bits, e=3105813805601888206905)
    file = open('./' + file_name + '.pem', 'w+')
    file.write(new_key.exportKey('PEM'))
    file.close()


def load_key(file_name='rsa_key_inj.pem'):

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


public_key, private_key = load_key()
N_int_array(public_key)
print ''
E_int_array(public_key)

# generate_RSA('rsa_test')