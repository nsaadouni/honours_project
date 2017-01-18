from virtualsmartcard.cards.Relay import RelayOS
from virtualsmartcard.VirtualSmartcard import VirtualICC
import binascii as ba

# vc = RelayOS(2) # works fine

emulator = VirtualICC(None, None, 'relay', 'localhost', 35963, 2)

emulator.run()



