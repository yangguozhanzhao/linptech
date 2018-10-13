from enum import Enum

class SerialConfig:
    RECEIVE_LEN_LIST = [21,22,23,29]
    SEND_INTERVAL = 0.01

class ReceiverType:
    R3AC = "81"
    RX_4 = "84"
    ALL = [R3AC,RX_4]

class ReceiverChannel:
    c1 = "01"
    c2 = "02"
    c3 = "04"
    c4 = "08"
    c1234 = "0f"
    ALL = [c1, c2, c3, c4, c1234]

class TransmitType:
    K5 = "02"
    K4R = "01"
    ALL = [K5, K4R]

# 开关通道
class TransmitChannel:
    c0 = "00"
    c1 = "01"
    c2 = "02"
    c3 = "04"
    ALL = [c0, c1, c2, c3]


# 报文类型
class PacketType:
    switch = "00" #模拟发射器
    control = "5f"  # 控制接收器（开关查）
    control_back = "5e"  # 控制返回
    config = "5d"  # 配置接收器：配置id和配置中继
    config_back = "5c"  # 配置返回

# 控制字节
class CmdType:
    # 状态相关，用PacketType.control
    control_state = "02" 
    inquire_state = "01" 

    # id相关,用PacketType.config
    write_id = "0d" 
    delete_id = "0e"
    delete_all_id = "09"
    inquire_id = "0a"

    # 中继相关,用PacketType.config
    config_relay = "04"
    inquire_relay = "05"


# 控制状态
class State:
    on = "01"
    off = "00"

# 返回状态
class BackState:
    ok = "00"
    fail = "01"
    full = "02"
    unsupport = "03"
    on = "01"
    off = "00"
    transmit = "20"
