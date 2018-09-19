from linptech.serial_communicator import LinptechSerial
import linptech.constant as CON
import time
import logging

logging.getLogger().setLevel(logging.DEBUG)
print(CON.RECEIVE_LEN_LIST)
port ='/dev/tty.SLAB_USBtoUART'
def receive(data,optional):
	print(data,optional)
lp_serial=LinptechSerial(port,receive=receive)
lp_serial.setDaemon(True)
lp_serial.start()
while lp_serial.is_alive():
	time.sleep(5)
	lp_serial.send("1f80016CB7"+CON.R3AC+"020101")
	time.sleep(5)
	lp_serial.send("1f80016CB7"+CON.R3AC+"020100")
