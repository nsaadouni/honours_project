# attempt DER decoding
import pyasn1
import OpenSSL
import hexdump as h
import binascii as ba
import sys


cert_1 = [128, 1, 5, 129, 129, 128, 247, 181, 21, 114, 7, 34, 148, 111, 196, 8, 100, 203, 189, 175, 234, 85, 125, 189,
 		143, 85, 54, 176, 1, 194, 139, 46, 50, 182, 93, 69, 241, 116, 93, 56, 18, 11, 173, 157, 44, 3, 156, 34, 70,
 		104, 235, 46, 162, 140, 32, 149, 168, 46, 108, 168, 224, 109, 71, 242, 211, 30, 215, 1, 248, 21, 92, 173, 220,
 		 5, 112, 192, 147,178, 109, 116, 176, 155, 149, 230, 77, 140, 210, 252, 115, 62, 205, 15, 48, 104, 121, 165, 185,
 		 53, 242, 65, 63, 82, 173, 173, 50, 160, 153, 26, 24, 61, 204, 87, 126, 57, 218, 71, 83, 30, 103, 21, 171, 1, 112,
 		 127, 242, 71, 150, 113, 68, 35, 206, 123, 96, 103, 130, 129, 128, 60, 82, 210, 6, 137, 40, 146, 44, 171, 230, 60,
 		 78, 230, 223, 14, 210, 41, 241, 1, 190, 54, 196, 248, 84, 64, 86, 243, 74, 250, 141, 46, 155, 96, 245, 7, 188, 237,
 		 180, 68, 86, 104, 93, 130, 76, 196, 234, 215, 150, 32, 248, 197, 70, 166, 224, 22, 184, 171, 165, 216, 67, 41, 88,
 		 83, 119, 23, 9, 151, 170, 112, 104, 51, 158, 241, 65, 10, 95, 57, 217, 117, 36, 127, 58, 83, 99, 97, 71, 135, 135,
 		 127, 136, 150, 188, 187, 131, 161, 203, 209, 66, 224, 235, 153, 207, 52, 14, 202, 86, 79, 44, 87, 80, 110, 123, 26,
 		 252, 31, 144, 122, 224, 194]

cert_2 = [168, 93, 211, 48, 227, 92, 169, 0, 57]



cert_11 = [128,1, 5, 129, 129, 128, 247, 181, 21, 114, 7, 34, 148, 111, 196, 8, 100, 203, 189, 175, 234, 85, 125, 189,
 		143, 85, 54, 176, 1, 194, 139, 46, 50, 182, 93, 69, 241, 116, 93, 56, 18, 11, 173, 157, 44, 3, 156, 34, 70,
 		104, 235, 46, 162, 140, 32, 149, 168, 46, 108, 168, 224, 109, 71, 242, 211, 30, 215, 1, 248, 21, 92, 173, 220,
 		 5, 112, 192, 147,178, 109, 116, 176, 155, 149, 230, 77, 140, 210, 252, 115, 62, 205, 15, 48, 104, 121, 165, 185,
 		 53, 242, 65, 63, 82, 173, 173, 50, 160, 153, 26, 24, 61, 204, 87, 126, 57, 218, 71, 83, 30, 103, 21, 171, 1, 112,
 		 127, 242, 71, 150, 113, 68, 35, 206, 123, 96, 103]



# 61 09 (9 more bytes to come)
SW_1 = [97, 9]
# 90 00 complete successfully
SW_2 = [144, 0]


cert_int = cert_1
for i in cert_2:
	cert_int.append(i)

cert_ascii = []
for i in cert_int:
	cert_ascii.append(chr(i))
cert_ascii = ''.join(cert_ascii)




cert_hex =[]
for i in cert_ascii:
	cert_hex.append(ba.hexlify(i))



# save this as a DER file, open with openssl
def print_der():

	out = []
	for i in range(0,263,2):
		out.append(cert_hex[i]+cert_hex[i+1])

	out.append(cert_hex[-1])

	counter = 0
	for i in range(16):
		for j in range(8):
			sys.stdout.write(out[counter] +'')
			counter+=1

	for i in range(5):
		sys.stdout.write(out[counter] +'')
		counter+=1




# page 20 id_protect_1.0 -> suggests x509 certifacte used to store the ECC CDH Z function Keys

# x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ANS1, cert_ascii)
# pk = x509.get_pubkey()

################################################################################################
#									Running Area											   #
################################################################################################

# print '\nlength of certificat believed to be ANS.1 X509 = ' +str(len(cert_int)) + ' bytes\n'
# h.hexdump(cert_ascii)
# print '\n\n'

# print public key found in the encoding
# print(pk)


# print_der()

# sys.stdout.write(cert_ascii)
print ''.join(cert_hex)




