from linptech.serial_communicator import LinptechSerial
from linptech.constant import (SerialConfig,ReceiverChannel,ReceiverType,
TransmitType,TransmitChannel,PacketType,CmdType,State,BackState)
import time
import logging

logging.getLogger().setLevel(logging.ERROR)
print(SerialConfig.RECEIVE_LEN_LIST)
port ='/dev/tty.SLAB_USBtoUART'
#port='COM3'
r_id="800172ea"
r_type = ReceiverType.R3AC
r_channel = ReceiverChannel.c1

t_id="000b0952"
t_type=TransmitType.K5
t_channel=TransmitChannel.c0

def receive(data,optional):
	#print("example, data=%s,optional=%s" %  (data,optional))
	if (PacketType.state_back+r_id + r_type + CmdType.write_state + r_channel + BackState.on) in data:
		print(">>>>>被测接收器打开")
	elif (PacketType.state_back+r_id + r_type + CmdType.write_state + r_channel + BackState.off) in data:
		print(">>>>>被测接收器关闭")
	elif (PacketType.state_back+r_id + r_type + CmdType.read_all_id + r_channel + BackState.off) in data:
		print(">>>>被测接收器状态为%s" % data[-2:])
	elif (PacketType.config_back+r_id + r_type + CmdType.write_id + BackState.ok) in data:
		print(">>>>>写入被测接收器id%s" % data[-2:])
	elif (PacketType.config_back+r_id + r_type + CmdType.delete_id + BackState.ok) in data:
		print(">>>> 删除被测接收器id%s" % data[-2:])
	elif (PacketType.config_back+r_id + r_type + CmdType.delete_all_id + BackState.ok) in data:
		print(">>>> 删除接收器所有id%s" % data[-2:])
	elif (PacketType.config_back+r_id + r_type + CmdType.write_relay + BackState.ok) in data:
		print(">>>> 设置接收器中继%s" % data[-2:])
	elif (PacketType.config_back+r_id + r_type + CmdType.read_relay + BackState.on ) in data:
		print(">>>> 被测接收器中继是%s" % data[-2:])
	elif (PacketType.config_back+r_id+r_type+CmdType.read_id_len+r_channel) in data:
		print(">>>>> 被测接收器通道中id长度为%s" % data[-4:])
	elif (PacketType.config_back+r_id+r_type+CmdType.read_one_id+r_channel) in data:
		print(">>>>> 被测接收器通道中指定序号id为%s" % data[-12:])


lp_serial=LinptechSerial(port,receive)
lp_serial.setDaemon(True)
lp_serial.start()


test_commands={
	"1模拟开关": PacketType.switch +t_id+t_type +"2"+t_channel[-1],
	"2打开接收器": PacketType.state +r_id+r_type +CmdType.write_state +r_channel +State.on, 
	"3关闭接收器": PacketType.state +r_id+r_type +CmdType.write_state +r_channel +State.off,
	"4查询接收器状态": PacketType.state +r_id+r_type+CmdType.read_state,

	"5写入id":PacketType.config +r_id+r_type+CmdType.write_id+r_channel+t_type+t_channel+t_id,
	"5.1读取指定通道id长度":PacketType.config+r_id+r_type+CmdType.read_id_len+r_channel,
	"5.2读取指定序号的单条id":PacketType.config+r_id+r_type+CmdType.read_one_id+r_channel+"01",
	"5.2读取指定序号的单条id":PacketType.config+r_id+r_type+CmdType.read_one_id+r_channel+"02",
	"5.2读取指定序号的单条id":PacketType.config+r_id+r_type+CmdType.read_one_id+r_channel+"03",
	"6读取指定通道所有id":PacketType.config +r_id+r_type + CmdType.read_all_id + r_channel,
	"7删除id":PacketType.config +r_id+r_type+CmdType.delete_id+r_channel+t_type+t_channel+t_id,
	"8删除所有id":PacketType.config+r_id+r_type+CmdType.delete_all_id+r_channel,
	"9开中继":PacketType.config+r_id+r_type+CmdType.write_relay+State.on,
	"10查询中继":PacketType.config+r_id+r_type+CmdType.read_relay,
	"11关闭中继":PacketType.config+r_id+r_type+CmdType.write_relay+State.off,
}

while lp_serial.is_alive():
	for name,command in test_commands.items():
		print(name,command)
		lp_serial.send(command)
		time.sleep(1)