from enum import Enum

# serial_communicator
RECEIVE_LEN_LIST=[21,22,23,29]
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
}
transmit_type={
    "K5":"02",
    "K4R":"01"
}
# 开关键值
transmit_channel={
    "c0":"00",
    "c1":"01",
    "c2":"02",
    "c3":"04",
}

# 报文类型
packet_type={
    "switch":"00",
    "operate_state":"5f", # 控制状态
    "show_state":"5e",# 状态返回
    "operate_config":"5d", # 操作配置,写入id和配置中继
    "show_config":"5c",# 配置返回
}

# 控制字节
cmd_type={
    "control_state":"02", # 状态相关
    "inquire_state":"01", #

    "write_id":"0d", # 配置相关
    "delete_id":"0e",
    "delete_all_id":"09",
    "inquire_id":"0a",

    "control_relay":"04",
    "inquire_relay":"05",
}

# 接收器状态
receiver_state={
    "on":"01",
    "off":"00",
}

# 操作id状态
config_state={
    "ok":"00",
    "fail":"01",
    "full":"02",
    "unsupport":"03",
}
