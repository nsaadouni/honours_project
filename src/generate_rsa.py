from Crypto.PublicKey import RSA 


def hexstring_to_intarray(x):
    out = []
    if len(x) % 2 != 0:
        x = '0' + x

    for i in range(0,len(x), 2):
        out.append(int((x[i]+x[i+1]),16))
        # ba.unhexlify(x[i]+x[i+1])
    return out

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    new_key = RSA.generate(bits, e=3105813805601888206905)
    public_key = new_key.publickey()
    private_key = new_key
    return private_key, public_key

private_key, public_key = generate_RSA()

print len(hex(public_key.__getattr__('n'))[2:-1])
print len(hex(public_key.__getattr__('e'))[2:-1])
print 'this seems like the correct public key format!'
print hexstring_to_intarray(hex(public_key.__getattr__('n'))[2:-1])


# new_key_2 = RSA.importKey(public_key)
# print new_key_2.size()
# print new_key_2.can_encrypt()
# print new_key_2.has_private()
# print new_key_2.keydata
# print len(hex(new_key_2.__getattr__('n'))[2:-1])/2

#-------------------------------------------------------------------------#

# this is the public key of the card!
# I now want to inject my own

n = '80 01 05 81 81 80 f7 b5 15 72 07 22 94 6f c4 08 64 cb bd af ea 55 7d bd 8f 55 36 b0 01 c2 8b 2e 32 b6 5d 45 f1 74 5d 38 12 0b ad 9d 2c 03 9c 22 46 68 eb 2e a2 8c 20 95 a8 2e 6c a8 e0 6d 47 f2 d3 1e d7 01 f8 15 5c ad dc 05 70 c0 93 b2 6d 74 b0 9b 95 e6 4d 8c d2 fc 73 3e cd 0f 30 68 79 a5 b9 35 f2 41 3f 52 ad ad 32 a0 99 1a 18 3d cc 57 7e 39 da 47 53 1e 67 15 ab 01 70 7f f2 47 96 71 44 23 ce 7b 60 67 82 81 80 3c 52 d2 06 89 28 92 2c ab e6 3c 4e e6 df 0e d2 29 f1 01 be 36 c4 f8 54 40 56 f3 4a fa 8d 2e 9b 60 f5 07 bc ed b4 44 56 68 5d 82 4c c4 ea d7 96 20 f8 c5 46 a6 e0 16 b8 ab a5 d8 43 29 58 53 77 17 09 97 aa 70 68 33 9e f1 41 0a 5f 39 d9 75 24 7f 3a 53 63 61 47 87 87 7f 88 96 bc bb 83 a1 cb d1 42 e0 eb 99 cf 34 0e ca 56 4f 2c 57 50 6e 7b 1a fc 1f 90 7a e0 '
modulus = ''.join(n.split())

e = 'a8 5d d3 30 e3 5c a9 00 39'
exponent = ''.join(e.split())

modulus = int(modulus, 16)
exponent = int(exponent, 16)

public_key_test = RSA.construct((modulus, exponent))

print public_key_test.keydata
print public_key_test.__getattr__('e')
t = public_key_test.encrypt('hello', None)
print len(t[0])
########################################################################################################################

"""
steps:
    1. get card public key
    2. open secure messaging
    3. select file
    4. create block cipher key

Plan:
    1.  create 2048 bit RSA key
        SAVE KEY FOR EASY LOAD!


        use 'n' and 'e' raw bytes to replace the card public key
        decrypt open secure messaging to see how long the command acutally is (keep in mind MAC)

    2. Figure out how the secure messaging operates (once we have this we have the block cipher keys!)
"""







































########################################################################################################################
from math import *

def isprime(n):
    '''check if integer n is a prime'''
    # make sure n is a positive integer
    n = abs(int(n))
    # 0 and 1 are not primes
    if n < 2:
        return False
    # 2 is the only even prime number
    if n == 2:
        return True
    # all other even numbers are not primes
    if not n & 1:
        return False
    # range starts with 3 and only needs to go up the squareroot of n
    # for all odd numbers
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True

# print isprime(public_key_test.__getattr__('e'))
########################################################################################################################







