import sys
import threading
import time
import serial
import binascii
from linptech.packet import Packet
import linptech.constant as CON
import logging
try:
	import queue
except ImportError:
	import Queue as queue

class LinptechSerial(threading.Thread):
	"""
	- 实例化线程进行串口发送和读取
	send_queue 发送指令队列
	receive_queue 接收指令队列
	"""
	def __init__(self, port, receive):
		super(LinptechSerial, self).__init__()
		self.stop_flag = threading.Event()
		self.buffer = ""
		# Setup packet queues
		self.send_queue = queue.Queue()
		self.receive_queue = queue.Queue()
		# Set the receive method，对外接口，接收指令
		self.receive = receive
		# Internal variable for the Base ID of the module.
		self.ser = serial.Serial(port, 57600, timeout=0.1)

	def stop(self):
		self.stop_flag.set()

	def send(self, data):
		"""对外接口，发送指令"""
		packet=Packet.create(data)
		self.send_queue.put(packet)
		logging.debug("send_queue=%s" % self.send_queue.qsize())
		return True
	
	def get_from_send_queue(self):
		""" Get message from transmit queue, if one exists """
		try:
			packet = self.send_queue.get(block=False)
			return packet
		except queue.Empty:
			pass
		return None

	def get_from_receive_queue(self):
		"""
		get packet from receive queue
		and as parameter pass to receive()
		"""
		while not self.receive_queue.empty()>0:
			try:
				logging.debug("receive_queue=%s" % self.receive_queue.qsize())
				packet=self.receive_queue.get()
				data,optional=Packet.parse(packet)
				self.receive(data,optional)
			except queue.Empty:
				pass

	def split_buffer(self,buffer):
		index = buffer.find("55",2*min(CON.RECEIVE_LEN_LIST))
		if int(index/2) in CON.RECEIVE_LEN_LIST :
			prev_buffer=buffer[0:index]
			if Packet.check(prev_buffer):
				self.receive_queue.put(prev_buffer)
			return buffer[index:]
		else:
			return buffer[index:]

	def run(self):
		"""
		run when self.start()
		threading.Thread function
		"""
		logging.debug('LinptechSerial started')
		while not self.stop_flag.is_set():
			try:
				number = self.ser.inWaiting()
				# print(number)
				if number >= min(CON.RECEIVE_LEN_LIST):
					logging.debug("numner=%s" % number)
					self.buffer += str(binascii.b2a_hex(self.ser.read(number)),encoding="utf-8")
					logging.debug("buffer=%s" % self.buffer)
					self.ser.flushInput()
					# 多组数据同时进入，进行递归分割
					while len(self.buffer) >= 4*min(CON.RECEIVE_LEN_LIST):
						self.buffer=self.split_buffer(self.buffer)
					if Packet.check(self.buffer):
						self.receive_queue.put(self.buffer)
			except serial.SerialException:
				print("error")
				logging.error('Serial port exception! (device disconnected or multiple access on port?)')
				self.stop()
			self.get_from_receive_queue()

			# # If there's messages in transmit queue，send them
			packet = self.get_from_send_queue()
			if packet:
				try:
					logging.debug("send_packet=%s",packet)
					self.ser.write(binascii.unhexlify(packet))
				except serial.SerialException:
					self.stop()
			time.sleep(CON.SEND_INTERVAL)

if __name__=="__main__":
	logging.getLogger().setLevel(logging.DEBUG)
	print(CON.RECEIVE_LEN_LIST)
	#port ='/dev/tty.SLAB_USBtoUART'
	port ="COM3"
	def receive(data,optional):
		print(data,optional)
	lp_serial=LinptechSerial(port,receive=receive)
	lp_serial.setDaemon(True)
	lp_serial.start()
	while lp_serial.is_alive():
		time.sleep(5)
		#lp_serial.send("1f80016CB7"+CON.R3AC+"020101")
		time.sleep(5)
		#lp_serial.send("1f80016CB7"+CON.R3AC+"020100")