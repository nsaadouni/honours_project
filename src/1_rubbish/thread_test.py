import threading


class tet(threading.Thread):

	def __init__(self,x):
		super(tet,self).__init__()
		self.x = x
		self.start()

	def run(self):

		counter = 15
		while counter>0:
			print format("This is thread %i" %self.x)
			counter -= 1



# t1 = tet(1)
# t2 = tet(2)

# t1.join()
# t2.join()

# It works!!!
#--------------------------------------------------

"""
This is the format I will use 
2 functions 2 differente threads:
	
	1. start man in the middle tool on second socket for accessing API (THREAD 1 -> has to be started first)
	2. PKCS11 C_login
"""


def simple_function(x):

	counter = 15
	while counter>0:
		print format("This is thread %i" %x)
		counter -= 1


t1 = threading.Thread(target=simple_function, args=(1,))
t2 = threading.Thread(target=simple_function, args=(2,))

t1.start()
t2.start()

# this works as well .... seems easier since I do not need CLASESES!
