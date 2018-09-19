import unittest
from linptech.crc8 import crc8
from linptech.packet import Packet
from linptech.serial_communicator import LinptechSerial

class Test(unittest.TestCase):
	"""test crc8.py"""

	def test_crc8(self):
		self.assertEqual(crc8("00070701"),'7a')
		self.assertEqual("0e",crc8("00150701"))
	
	def test_packet_create(self):
		data="1f8000004581020101"
		optional="00"*7
		packet="550009070156"+data+optional+"3c"
		self.assertEqual(Packet.create(data),packet)
	
	def test_packet_check(self):
		data="1f8000004581020101"
		optional="00"*7
		packet="550009070156"+data+optional+"3c"
		self.assertTrue(Packet.check(packet))
		packet_false="550009070156"+data+optional+"4c"
		self.assertFalse(Packet.check(packet_false))

	def test_packet_parse(self):
		data="1f8000004581020101"
		optional="00"*7
		packet="550009070156"+data+optional+"3c"
		packet_data,packet_optional=Packet.parse(packet)
		self.assertEqual(data,packet_data)
		self.assertEqual(optional,packet_optional)
	
	def test_linptech_serial(self):
		data="1f8000004581020101"
		ser=LinptechSerial('/dev/tty.SLAB_USBtoUART',receive=None)
		self.assertEqual(ser.send_queue.qsize(),0)
		ser.send(data)
		self.assertEqual(ser.send_queue.qsize(),1)
		self.assertEqual(ser.send_queue.get(),Packet.create(data))

if __name__ == '__main__':
	unittest