from linptech.constant import (SerialConfig,ReceiverChannel,ReceiverType,
TransmitType,TransmitChannel,PacketType,CmdType,State,BackState)
from linptech.linptech_protocol import LinptechProtocol
import time
import logging
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import platform

logging.getLogger().setLevel(logging.DEBUG)

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry('1024x320')  
		self.wm_title('linptech射频协议串口测试')
		
		# 串口设置
		if platform.system()=="Darwin":
			port=self.get_port()[-1]
		else:
			port=self.get_port()[0]
		self.lp=LinptechProtocol(port,receive=self.receive)
		self.create_widgets()
	
	def get_port(self):
		portList = list(serial.tools.list_ports.comports())
		portNameList = []
		for port in portList:
			portNameList.append(str(port[0]))
		logging.debug("portNameList=%s",portNameList)
		return portNameList
	
	def create_widgets(self):
		# 被测设备
		device_lf=ttk.LabelFrame(self, text='被测设备')
		device_lf.grid(column=0, row=0,padx=15,pady=4,sticky='w')

		self.is_listen_receiver = tk.IntVar()
		self.rssi_threshold_receiver = tk.IntVar()
		self.rssi_threshold_receiver.set("70")

		ttk.Checkbutton(device_lf, text="监听接收器",width=10,variable=self.is_listen_receiver).grid(row=0,column=0,)
		ttk.Label(device_lf,text="RSSI阈值：").grid(row=0,column=1)
		tk.Spinbox(device_lf, from_=40,to=95,width=3,textvariable=self.rssi_threshold_receiver,wrap=True) .grid(row=0,column=2)

		self.receiver_id=tk.StringVar()
		self.receiver_type=tk.StringVar()
		self.receiver_channel=tk.StringVar()
		self.receiver_rssi=tk.StringVar()
		
		ttk.Label(device_lf,text="接收器ID").grid(row=0,column=3,sticky='e')
		ttk.Entry(device_lf,textvariable=self.receiver_id,width=8).grid(row=0,column=4)
		ttk.Label(device_lf,text="接收器类型值").grid(row=0,column=5,sticky='e')
		ttk.Combobox(device_lf,values=ReceiverType.ALL,textvariable=self.receiver_type,width=3).grid(row=0,column=6)
		ttk.Label(device_lf,text="接收器通道值").grid(row=0,column=7,sticky='e')
		ttk.Combobox(device_lf,values=ReceiverChannel.ALL,textvariable=self.receiver_channel,width=3).grid(row=0,column=8)
		ttk.Label(device_lf,text="接收器信号强度").grid(row=0,column=9,sticky='e')
		ttk.Entry(device_lf,textvariable=self.receiver_rssi,width=3).grid(row=0,column=10)


		self.is_listen_transmit = tk.IntVar()
		self.rssi_threshold_transmit = tk.IntVar()
		self.rssi_threshold_transmit.set("70")

		ttk.Checkbutton(device_lf, text="监听发射器",width=10,variable=self.is_listen_transmit).grid(row=1,column=0,)
		ttk.Label(device_lf,text="RSSI阈值：").grid(row=1,column=1)
		tk.Spinbox(device_lf, from_=40,to=95,width=3,textvariable=self.rssi_threshold_transmit,wrap=True) .grid(row=1,column=2)

		self.transmit_id=tk.StringVar()
		self.transmit_type=tk.StringVar()
		self.transmit_channel=tk.StringVar()
		self.transmit_rssi=tk.StringVar()
		ttk.Label(device_lf,text="发射器ID").grid(row=1,column=3,sticky='e')
		ttk.Entry(device_lf,textvariable=self.transmit_id,width=8).grid(row=1,column=4)
		ttk.Label(device_lf,text="发射器类型值").grid(row=1,column=5,sticky='e')
		ttk.Combobox(device_lf,values=TransmitType.ALL,textvariable=self.transmit_type,width=3).grid(row=1,column=6)
		ttk.Label(device_lf,text="发射器通道值").grid(row=1,column=7,sticky='e')
		ttk.Combobox(device_lf,values=TransmitChannel.ALL,textvariable=self.transmit_channel,width=3).grid(row=1,column=8)
		ttk.Label(device_lf,text="发射器信号强度").grid(row=1,column=9,sticky='e')
		ttk.Entry(device_lf,textvariable=self.transmit_rssi,width=3).grid(row=1,column=10)

		# 操作
		command_lf=ttk.LabelFrame(self, text='操作按钮')
		command_lf.grid(column=0, row=1,padx=15,pady=4,sticky="w")

		ttk.Button(command_lf,text="模拟开关on",command=lambda : \
		self.lp.switch_on(self.transmit_id.get(),self.transmit_type.get(),self.transmit_channel.get()))\
		.grid(row=0,column=0)

		ttk.Button(command_lf,text="模拟开关off",command=lambda : \
		self.lp.switch_off(self.transmit_id.get(),self.transmit_type.get(),self.transmit_channel.get()))\
		.grid(row=0,column=1)

		ttk.Button(command_lf,text="打开接收器",command=lambda : \
		self.lp.set_receiver_on(self.receiver_id.get(),self.receiver_type.get(),self.receiver_channel.get()))\
		.grid(row=1,column=0)

		ttk.Button(command_lf,text="关闭接收器",command=lambda : \
		self.lp.set_receiver_off(self.receiver_id.get(),self.receiver_type.get(),self.receiver_channel.get()))\
		.grid(row=1,column=1)

		ttk.Button(command_lf,text="读接收器状态",command=lambda : \
		self.lp.read_receiver_state(self.receiver_id.get(),self.receiver_type.get()))\
		.grid(row=1,column=2)

		ttk.Button(command_lf,text="打开接收器中继",command=lambda : \
		self.lp.set_receiver_relay(self.receiver_id.get(),self.receiver_type.get(),State.on))\
		.grid(row=2,column=0)

		ttk.Button(command_lf,text="关闭接收器中继",command=lambda : \
		self.lp.set_receiver_relay(self.receiver_id.get(),self.receiver_type.get(),State.off))\
		.grid(row=2,column=1)

		ttk.Button(command_lf,text="读取接收器中继",command=lambda : \
		self.lp.read_receiver_relay(self.receiver_id.get(),self.receiver_type.get()))\
		.grid(row=2,column=2)

		ttk.Button(command_lf,text="清除接收器所有配对",command=lambda : \
		self.lp.delete_all_id(self.receiver_id.get(),self.receiver_type.get(),self.receiver_channel.get()))\
		.grid(row=3,column=0)

		ttk.Button(command_lf,text="读取接收器当前通道配对长度",command=lambda : \
		self.lp.read_id_length(self.receiver_id.get(),self.receiver_type.get(),self.receiver_channel.get()))\
		.grid(row=3,column=1)

		ttk.Button(command_lf,text="读取接收器当前通道序号1的id",command=lambda : \
		self.lp.read_one_id(self.receiver_id.get(),self.receiver_type.get(),self.receiver_channel.get(),index="01"))\
		.grid(row=3,column=2)

		ttk.Button(command_lf,text="配对接收器发射器",command=lambda : \
		self.lp.write_transmit_to_receiver(self.receiver_id.get(),self.receiver_type.get(),self.receiver_channel.get(),\
		self.transmit_id.get(),self.transmit_type.get(),self.transmit_channel.get()))\
		.grid(row=4,column=0)
		ttk.Button(command_lf,text="删除接收器发射器配对",command=lambda : \
		self.lp.delete_one_id(self.receiver_id.get(),self.receiver_type.get(),self.receiver_channel.get(),\
		self.transmit_id.get(),self.transmit_type.get(),self.transmit_channel.get()))\
		.grid(row=4,column=1)

		# 返回信息
		log_lf=ttk.LabelFrame(self, text='返回信息')
		log_lf.grid(column=0, row=2,padx=15,pady=4,sticky="w")
		self.info=tk.StringVar()
		ttk.Label(log_lf,textvariable=self.info).grid(row=1,column=0)

	def receive(self,data,optional):
		"""
		必须处理self.lp.forecast_list
		"""
		logging.debug('data=%s,optional=%s' % (data,optional))
		logging.debug('forecast=%s' % self.lp.forecasts)
		# 删除count>3的，删除与back相等的
		# 重发改变count,改变timestamp
		for f in self.lp.forecasts: 
			if f["count"]>3:
				print("超过次数清除")
				self.lp.forecasts.remove(f)
			elif data.startswith(f["back"]):
				print("获取返回清除")
				self.lp.forecasts.remove(f)
				self.info.set(f["info"]+data[f["info_index"]:f["info_index"]+f["info_len"]])
			elif time.time()-f["timestamp"] > 0.2:
				print("再次发送")
				f["count"]+=1
				f["timestamp"]=time.time()
				self.lp.ser.send(f["data"])
		# 监听接收器
		if (self.is_listen_receiver.get()==1) and (data[10:12] in ReceiverType.ALL):
			if (int(optional[0:2],16)<self.rssi_threshold_receiver.get()):
				self.receiver_id.set(data[2:10])
				self.receiver_type.set(data[10:12])
				self.receiver_channel.set(data[12:14])
				self.receiver_rssi.set(int(optional[0:2],16))
		if (self.is_listen_transmit.get()==1):
			if (data[10:12] in TransmitType.ALL):
				if (int(optional[0:2],16)<self.rssi_threshold_transmit.get()):
					self.transmit_id.set(data[2:10])
					self.transmit_type.set(data[10:12])
					self.transmit_channel.set(data[12:14])
					self.transmit_rssi.set(int(optional[0:2],16))
		

if __name__ == '__main__':
	r_id="8001734d"
	t_id="00089a6b"

	app = App()
	app.receiver_id.set(r_id)
	app.receiver_type.set(ReceiverType.R3AC)
	app.receiver_channel.set(ReceiverChannel.c1)
	app.transmit_id.set(t_id)
	app.transmit_type.set(TransmitType.K5)
	app.transmit_channel.set(TransmitChannel.c0)
	def closeWindow():
		app.destroy()
	app.protocol('WM_DELETE_WINDOW', closeWindow) 
	app.mainloop()