from linptech.serial_communicator import LinptechSerial
import linptech.constant as CON
import time
import logging

logging.getLogger().setLevel(logging.DEBUG)
print(CON.RECEIVE_LEN_LIST)
port ='/dev/tty.SLAB_USBtoUART'
#port='/dev/ttyS0'
def receive(data,optional):
	print("e,data=%s,optional=%s" %  (data,optional))
lp_serial=LinptechSerial(port,receive)
lp_serial.setDaemon(True)
lp_serial.start()
receiver_id="800172ea"
transmit_id="000b0952"

test_commands={
	"模拟开关": CON.packet_type["switch"]+transmit_id+CON.transmit_type["K5"]+"2"+CON.transmit_channel["c0"][-1],
	"打开接收器": CON.packet_type["operate_state"]+receiver_id+CON.receiver_type["R3AC"]+\
				CON.cmd_type["control_state"]+CON.receiver_channel["c1"]+CON.receiver_state["on"], 
	"关闭接收器": CON.packet_type["operate_state"]+receiver_id+CON.receiver_type["R3AC"]+\
				CON.cmd_type["control_state"]+CON.receiver_channel["c1"]+CON.receiver_state["off"],
	"查询接收器状态": CON.packet_type["operate_state"]+receiver_id+CON.receiver_type["R3AC"]+CON.cmd_type["inquire_state"],
	"写入id":CON.packet_type["operate_config"]+receiver_id+CON.receiver_type["R3AC"]+\
			CON.cmd_type["write_id"]+CON.receiver_channel["c1"]+CON.transmit_type["K5"]\
			+CON.transmit_channel["c0"]+transmit_id,
	"查询指定通道id":CON.packet_type["operate_config"]+receiver_id+CON.receiver_type["R3AC"]+\
					CON.cmd_type["inquire_id"]+CON.receiver_channel["c1"],
	"删除id":CON.packet_type["operate_config"]+receiver_id+CON.receiver_type["R3AC"]+\
			CON.cmd_type["delete_id"]+CON.receiver_channel["c1"]+CON.transmit_type["K5"]\
			+CON.transmit_channel["c0"]+transmit_id,
	"删除所有id":CON.packet_type["operate_config"]+receiver_id+CON.receiver_type["R3AC"]+\
				CON.cmd_type["delete_all_id"]+CON.receiver_channel["c1"],
	"开中继":CON.packet_type["operate_config"]+receiver_id+CON.receiver_type["R3AC"]+\
			CON.cmd_type["control_relay"]+CON.receiver_state["on"],
	"查询中继":CON.packet_type["operate_config"]+receiver_id+CON.receiver_type["R3AC"]+\
				CON.cmd_type["inquire_relay"],
	"关闭中继":CON.packet_type["operate_config"]+receiver_id+CON.receiver_type["R3AC"]+\
			CON.cmd_type["control_relay"]+CON.receiver_state["off"]
}

while lp_serial.is_alive():
	for name,command in test_commands.items():
		print(name)
		lp_serial.send(command)
		time.sleep(1)