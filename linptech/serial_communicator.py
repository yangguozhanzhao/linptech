import sys
import threading
import time
import serial
import binascii
from linptech.packet import Packet
from linptech.constant import SerialConfig
import logging
try:
	import queue
except ImportError:
	import Queue as queue

logging.getLogger().setLevel(logging.ERROR)

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
		self.port = port
		self.ser = serial.Serial(self.port, 57600, timeout=0.1)
		self.restart_num=0

	def restart(self):
		self.stop_flag.set()
		self.ser.close()
		while self.stop_flag.is_set():
			time.sleep(2)
			try:
				number = self.ser.inWaiting()
				self.stop_flag.clear()
				self.run()
			except Exception as e:
				self.restart_num+=1
				logging.error("reconnect serialport %d",self.restart_num)
				try:
					self.stop_flag.set()
					self.ser = serial.Serial(self.port, 57600, timeout=0.1)
				except Exception as e:
					logging.error(e)

	def send(self, data):
		"""对外接口，发送指令"""
		try:
			packet=Packet.create(data)
			self.send_queue.put(packet)
			logging.debug("send_queue=%s" % self.send_queue.qsize())
			return True
		except Exception as e:
			logging.error("send error:%s",e)
			
		
	
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
		while not self.receive_queue.empty():
			try:
				logging.debug("receive_queue=%s" % self.receive_queue.qsize())
				packet=self.receive_queue.get()
				data,optional=Packet.parse(packet)
				self.receive(data,optional)
			except queue.Empty:
				pass

	def process_buffer(self,buffer):
		if len(buffer) > 2*max(SerialConfig.RECEIVE_LEN_LIST):
			try:
				index = buffer.find("550",2*min(SerialConfig.RECEIVE_LEN_LIST))
				if int(index/2) in SerialConfig.RECEIVE_LEN_LIST :
					prev_buffer=buffer[0:index]
					if Packet.check(prev_buffer):
						self.receive_queue.put(prev_buffer)
				self.process_buffer(buffer[index:])
			except Exception as e:
				logging.error("process buffer error:%s" % e)
		elif len(buffer)/2 in SerialConfig.RECEIVE_LEN_LIST and Packet.check(buffer):
			self.receive_queue.put(buffer)

	def run(self):
		"""
		run when self.start()
		threading.Thread function
		"""
		logging.debug('LinptechSerial started')
		while not self.stop_flag.is_set():
			for i in range(10):
				time.sleep(SerialConfig.SEND_INTERVAL)
				
				try:
					number = self.ser.inWaiting()
					# print(number)
					if number >= min(SerialConfig.RECEIVE_LEN_LIST):
						self.buffer += str(binascii.b2a_hex(self.ser.read(number)),encoding="utf-8")
						logging.debug("numner=%s,self.buffer=%s" % (number,self.buffer))
						self.ser.flushInput()
						# 多组数据同时进入，进行递归分割
						self.process_buffer(self.buffer)
						self.buffer=""
					self.get_from_receive_queue()
				except Exception as e:
					logging.error("run serial read data error:%s" % e)
					self.restart()
				
			# # If there's messages in transmit queue，send them
			packet = self.get_from_send_queue()
			if packet:
				try:
					logging.debug("send_packet=%s",packet)
					self.ser.write(binascii.unhexlify(packet))
				except Exception as e:
					logging.error("run serial write data error:%s" % e)
					self.restart()

if __name__=="__main__":
	logging.getLogger().setLevel(logging.DEBUG)
	print(SerialConfig.RECEIVE_LEN_LIST)
	port ='/dev/tty.SLAB_USBtoUART'
	#port ="COM3"
	def receive(data,optional):
		print(data,optional)
	lp_serial=LinptechSerial(port,receive=receive)
	lp_serial.setDaemon(True)
	lp_serial.start()
	while lp_serial.is_alive():
		time.sleep(5)

