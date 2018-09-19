from linptech.crc8 import crc8
import logging

class Packet(object):
	'''
	Base class for Packet.
	Mainly used for for packet generation and
	Packet.parse_msg(buf) for parsing message.
	parse_msg() returns subclass, if one is defined for the data type.
	'''	
	def __init__(self, data=None, optional="00"*7):
		if  data is None:
			logging.warning('Packet.data is None')
		else:
			self.data = data

		if optional is None:
			logging.info('Packet.optional is None.')
		else:
			self.optional = optional
	
	@staticmethod
	def check(packet):
		"""
		check packet with crc
		"""
		if packet.startswith("55") and \
		crc8(packet[2:10])==packet[10:12] and \
		crc8(packet[12:-2])==packet[-2:]:
			return True
		else:
			return False
	@staticmethod
	def parse(packet):
		"""
		parse an packet to data and optional for receive
		"""
		if Packet.check(packet):
			data_len=int(packet[4:6],16)
			data=packet[12:12+data_len*2]
			optional=packet[12+data_len*2:26+data_len*2]
			return data,optional
		else :
			logging.info("packet is invalid")
			return
	
	@staticmethod
	def create(data=None, optional="00"*7):
		"""
		Creates an packet ready for sending.
		Uses data and optional.
		"""
		data_len = "{0:>02}".format(hex(int(len(data)/2))[2:])
		m1 = "00"+data_len+"0701"
		m2 = data+optional
		packet = "55"+m1+crc8(m1)+m2+crc8(m2)
		#logging.debug("packet=%s",packet)
		return packet
if __name__ == "__main__":
	logging.getLogger().setLevel(logging.INFO)
	data="1f8000004581020101"
	Packet.create(data)