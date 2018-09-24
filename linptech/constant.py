from enum import Enum

# serial_communicator
RECEIVE_LEN_LIST=[21,23]
SEND_INTERVAL=0.01

receiver_type={
    "R3AC":"81",
    "RX_4":"84"
}
receiver_channel={
    "c1":"01",
    "c2":"02",
    "c3":"04",
    "c4":"08",
    "c1234":"0f",
    "c12":"03",
}
transmit_type={
    "K5":"01",
    "K4R":"02"
}
# 开关键值
transmit_key={
    "on_off":"20",
    "back":"00",
    "c1_on":"31",
    "c1_off":"21",
    "c2_on":"32",
    "c2_off":"22",
    "c3_on":"34",
    "c3_off":"24",
}

# 报文类型
packet_type={
    "switch":"00",
    "operate_state":"5f", #控制报文
    "show_state":"5e",#状态报文
    "operate_id":"5d",
    "show_id":"5c"
}

# 控制字节
cmd_type={
    "control_state":"02", #控制指令
    "inquire_state":"01",#状态报文
    "write_id":"0d",
    "delete_id":"0e",
    "delete_all_id":"09",
}

# 接收器状态
receiver_state={
    "on":"01",
    "off":"00",
}

# 操作id状态
id_state={
    "ok":"00",
    "fail":"01",
    "full":"02",
    "unsupport":"03",
}