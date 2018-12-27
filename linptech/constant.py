from enum import Enum

class SerialConfig:
    RECEIVE_LEN_LIST = [21,22,23,24,29] #对应返回长度 07，08，09，0a，0f
    SEND_INTERVAL = 0.015

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
    state = "5f"  # 控制接收器（开关查）
    state_back = "5e"  # 控制返回
    config = "5d"  # 配置接收器：配置id和配置中继
    config_back = "5c"  # 配置返回

# 控制字节
class CmdType:
    # 状态相关，用PacketType.control
    read_state = "01"
    write_state = "02" 

    # id相关和中继,用PacketType.config

    # 01读取程序版本，
    # 02 配置上电默认输出，
    # 03 读取上电默认输出

    write_relay = "04"
    read_relay = "05"
    # 06配置心跳 07读取心跳

    read_id_len = "08"
    delete_all_id = "09"
    read_all_id = "0a"
    read_one_id="0b"
    read_id_exist="0c"
    write_id = "0d" 
    delete_id = "0e"


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
