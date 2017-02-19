from Crypto.PublicKey import RSA 
import binascii as ba
# from Crypto.PublicKey import ECC

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    new_key = RSA.generate(bits, e=65537) 
    public_key = new_key.publickey().exportKey("DER") 
    private_key = new_key.exportKey("DER")
    return private_key, public_key

private_key, public_key = generate_RSA()

# def generate_ECC():
# 	key = ECC.generate(curve='P-256')
# 	return key

# public_key = generate_ECC()

print public_key
print ''
print ba.hexlify(public_key)
print ''
print 'number of hexidecimal characters: ' + str(len(ba.hexlify(public_key)))
print 'number of bytes: ' + str(len(ba.hexlify(public_key))/2)
print 'looking for 512 hexidecmial characters (256 bytes) excluding the exponenet'