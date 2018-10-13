from linptech.serial_communicator import LinptechSerial
from linptech.constant import (SerialConfig,ReceiverChannel,ReceiverType,
TransmitType,TransmitChannel,PacketType,CmdType,State,BackState)
import time
import logging

logging.getLogger().setLevel(logging.DEBUG)
print(SerialConfig.RECEIVE_LEN_LIST)
#port ='/dev/tty.SLAB_USBtoUART'
port='COM3'
r_id="800172ea"
r_type = ReceiverType.R3AC
r_channel = ReceiverChannel.c1

t_id="000b0952"
t_type=TransmitType.K5
t_channel=TransmitChannel.c0

def receive(data,optional):
	print("e, data=%s,optional=%s" %  (data,optional))
	if (t_id + CmdType.control_state) in data:
		print("a模拟开关")
	elif (r_id + r_type + CmdType.control_state + r_channel + BackState.on) in data:
		print("a打开接收器")
	elif (r_id + r_type + CmdType.control_state + r_channel + BackState.off) in data:
		print("a关闭接收器")
	elif (r_id + r_type + CmdType.inquire_state + r_channel + BackState.off) in data:
		print("a查询接收器状态")
	elif (r_id + r_type + CmdType.write_id + BackState.ok) in data:
		print("a写入id")
	elif (r_id + r_type + CmdType.delete_id + BackState.ok) in data:
		print("a删除id")
	elif (r_id + r_type + CmdType.delete_all_id + BackState.ok) in data:
		print("a删除所有id")
	elif (r_id + r_type + CmdType.config_relay + BackState.ok) in data:
		print("a开中继或关中继")
	elif (r_id + r_type + CmdType.inquire_relay + BackState.on ) in data:
		print("a查询中继")
	else:
		print("A其他情况")


lp_serial=LinptechSerial(port,receive)
lp_serial.setDaemon(True)
lp_serial.start()


test_commands={
	"1模拟开关": PacketType.switch +t_id+t_type +"2"+t_channel[-1],
	"2打开接收器": PacketType.control +r_id+r_type +CmdType.control_state +r_channel +State.on, 
	"3关闭接收器": PacketType.control +r_id+r_type +CmdType.control_state +r_channel +State.off,
	"4查询接收器状态": PacketType.control +r_id+r_type+CmdType.inquire_state,
	"5写入id":PacketType.config +r_id+r_type+CmdType.write_id+r_channel+t_type+t_channel+t_id,
	"6查询指定通道id":PacketType.config +r_id+r_type + CmdType.inquire_id + r_channel,
	"7删除id":PacketType.config +r_id+r_type+CmdType.delete_id+r_channel+t_type+t_channel+t_id,
	"8删除所有id":PacketType.config+r_id+r_type+CmdType.delete_all_id+r_channel,
	"9开中继":PacketType.config+r_id+r_type+CmdType.config_relay+State.on,
	"10查询中继":PacketType.config+r_id+r_type+CmdType.inquire_relay,
	"11关闭中继":PacketType.config+r_id+r_type+CmdType.config_relay+State.off,
}

while lp_serial.is_alive():
	for name,command in test_commands.items():
		print(name,command)
		lp_serial.send(command)
		time.sleep(3)