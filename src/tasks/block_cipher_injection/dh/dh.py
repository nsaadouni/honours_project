import binascii as ba
import sys
import hashlib as hs
from CryptoPlus.Cipher import DES, DES3, AES



def hexstring_to_intarray(x):
    out = []
    if len(x) % 2 != 0:
        x = '0' + x

    for i in range(0,len(x), 2):
        out.append(int((x[i]+x[i+1]),16))
        # ba.unhexlify(x[i]+x[i+1])
    return out


def print_ints(command):

	for i in command:
		sys.stdout.write( str(i) +' ')
	print '\n'


############################################################


x_command = '0C 84 00 00 0D 97 01 18 8E 08 1C 0B 23 9F 34 B7 29 FD 00'
command = []
for i in x_command.split():
	command.append(int(i,16))

x_cmac = '1C 0B 23 9F 34 B7 29 FD'
cmac = []
for i in x_cmac.split():
	cmac.append(int(i,16))

shared_secret = '\x00'
shared_secret_128 = '\x00'*128

x_cards_challenge_for_smac = 'A5 F0 D1 FA AF 53 93 A7  49 8D 69 8B 7A 1A D0 A4'
cards_challenge_for_smac = []
for i in x_cards_challenge_for_smac.split():
	cards_challenge_for_smac.append((int(i,16)))
# cards_challenge_for_smac = ''.join(cards_challenge_for_smac)

##############################################################

# first hash the shared secret || carrds challenge (second 16 bytes for smac)
h = hs.new('sha1')
h.update('\x00')
k = h.digest()[0:16]
kk = []
for i in range(len(k)):
	kk.append(ord(k[i]) ^ cards_challenge_for_smac[i])

key = []
for i in kk:
	key.append(chr(i))
key = ''.join(key)


command_to_compute_cmac = [12, 132, 0, 0, 128, 0, 0, 0, 0,  151, 1, 24, 128, 0, 0, 0, 0, 0]

msg = []
for i in command_to_compute_cmac:
	msg.append(chr(i))
msg = ''.join(msg)


IVV = [0,0,0,0,0,0,0,0]
IV_8 = []
IV_16 = []
for i in IVV:
	IV_8.append(chr(i))
	IV_16.append(chr(i))
for i in IVV:
	IV_16.append(chr(i))
IV_8 = ''.join(IV_8)
IV_16 = ''.join(IV_16)


cipher1 = DES3.new(key, DES3.MODE_CBC, IV_8)
print ba.hexlify(cipher1.encrypt(msg))
cipher1 = DES3.new(key, DES3.MODE_CMAC, IV_8)
print ba.hexlify(cipher1.encrypt(msg))


cipher1 = AES.new(key, AES.MODE_CBC, IV_16)
print ba.hexlify(cipher1.encrypt(msg))
cipher1 = AES.new(key, AES.MODE_CMAC, IV_16)
print ba.hexlify(cipher1.encrypt(msg))