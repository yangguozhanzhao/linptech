from linptech.serial_communicator import LinptechSerial
import logging
from linptech.constant import (SerialConfig,ReceiverChannel,ReceiverType,
TransmitType,TransmitChannel,PacketType,CmdType,State,BackState)
import time


logging.getLogger().setLevel(logging.ERROR)

#liptech 设备协议的实现
class LinptechProtocol(object):
	def __init__(self,port,receive):
		self.ser=LinptechSerial(port,receive=receive)
		self.forecasts=[] # 存储发送和预接收的数据
		self.ser.setDaemon(True)
		self.ser.start()

	def check_repeat(self,id,forecasts):
		for f in forecasts:
			if id in f["back"]:
				forecasts.remove(f)
	# 模拟开关
	def switch_on(self,t_id,t_type,t_channel):
		self.ser.send(PacketType.switch +t_id+t_type +"3"+t_channel[-1])
	
	def switch_off(self,t_id,t_type,t_channel):
		self.ser.send(PacketType.switch +t_id+t_type +"2"+t_channel[-1])

	def set_receiver_on(self,r_id,r_type,r_channel):
		data = PacketType.state +r_id+r_type +CmdType.write_state +r_channel +r_channel
		back = PacketType.state_back+r_id+r_type+CmdType.write_state
		self.ser.send(data)
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"设置接收器状态为(00关/01开)","info_index":16,"info_len":2})
	
	def set_receiver_off(self,r_id,r_type,r_channel):
		data = PacketType.state +r_id+r_type +CmdType.write_state +r_channel +State.off
		back = PacketType.state_back+r_id+r_type+CmdType.write_state
		self.ser.send(data)
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"设置接收器状态为(00关/01开)","info_index":16,"info_len":2})

	def read_receiver_state(self,r_id,r_type):
		data = PacketType.state +r_id+r_type +CmdType.read_state
		back = PacketType.state_back+r_id+r_type+CmdType.read_state
		self.ser.send(data)
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"读取接收器状态(00关/01开)","info_index":14,"info_len":4})

	def set_receiver_relay(self,r_id,r_type,state=State.on):
		data=PacketType.config+r_id+r_type+CmdType.write_relay+state
		back=PacketType.config_back+r_id+r_type+CmdType.write_relay
		self.ser.send(data)
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"设置接收器中继(00成功/01失败)为","info_index":14,"info_len":2})
	
	def read_receiver_relay(self,r_id,r_type):
		data = PacketType.config+r_id+r_type+CmdType.read_relay
		back = PacketType.config_back+r_id+r_type+CmdType.read_relay
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"读取接收器状态(00关/01开)","info_index":14,"info_len":2})
		self.ser.send(data)
		
	def write_transmit_to_receiver(self,r_id,r_type,r_channel,t_id,t_type,t_channel):
		data = PacketType.config +r_id+r_type+CmdType.write_id+r_channel+t_type+t_channel+t_id
		back = PacketType.config_back +r_id+r_type+CmdType.write_id
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"发射器id写入接收器状态(00成功/01失败/02已满)为","info_index":14,"info_len":2})
		self.ser.send(data)
	
	def delete_one_id(self,r_id,r_type,r_channel,t_id,t_type,t_channel):
		data = PacketType.config +r_id+r_type+CmdType.delete_id+r_channel+t_type+t_channel+t_id
		back = PacketType.config_back +r_id+r_type+CmdType.delete_id
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"删除接收器中指定发射器id(00成功/01失败)","info_index":14,"info_len":2})
		self.ser.send(data)
	
	def delete_all_id(self,r_id,r_type,r_channel):
		data = PacketType.config+r_id+r_type+CmdType.delete_all_id+r_channel
		back = PacketType.config_back+r_id+r_type+CmdType.delete_all_id
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"清除接收器指定通道配对(00成功/01失败)","info_index":16,"info_len":2})
		self.ser.send(data)
	
	def read_id_length(self,r_id,r_type,r_channel):
		data = PacketType.config+r_id+r_type+CmdType.read_id_len+r_channel
		back = PacketType.config_back+r_id+r_type+CmdType.read_id_len+r_channel
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"读取接收器指定通道配对id个数","info_index":16,"info_len":2})
		self.ser.send(data)
	
	def read_one_id(self,r_id,r_type,r_channel,index="01"):
		data = PacketType.config+r_id+r_type+CmdType.read_one_id+r_channel+index
		back = PacketType.config_back+r_id+r_type+CmdType.read_one_id+r_channel
		self.check_repeat(r_id,self.forecasts)
		self.forecasts.append({"timestamp":time.time(),"count":1,"data":data,"back":back,
		"info":"读取接收器指定通道指定序号id(总数+序号-##-##-发射器id)","info_index":16,"info_len":14})
		self.ser.send(data)
	
	def read_all_id(self,r_id,r_type,r_channel):
		"""不稳，尽量不用"""
		self.ser.send(PacketType.config +r_id+r_type + CmdType.read_all_id + r_channel)