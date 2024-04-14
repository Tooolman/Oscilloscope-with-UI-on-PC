import serial
import numpy as np
import time

# 打开串口
ser = serial.Serial('COM4', 115200)  # 替换成你的串口号和波特率
#500unit16*2=  1000byte#2

# 定义开始信号、结束信号和确认信号
START_SIGNAL = 'SSTART\n'+18*'0'
FINISH_SIGNAL = 'FINISH\n'
CONFIRM_SIGNAL = 'ACKACK\n'
S1_HIGH = 'H1'+23*'0'

ser.reset_input_buffer()
ser.reset_output_buffer()

try:
    while True:
        # 发送开始信号给下位机
        ser.write(str(START_SIGNAL).encode('utf-8'))
        print("start signal written")
        while ser.readline().decode('utf-8') != CONFIRM_SIGNAL:
            print("waiting for confirm signal")
        
        print("confirm signal received")
#         data = ser.readline().decode('utf-8')
#         print('Received data:',data)
        
        byte_data_frame = ser.read(4000)
        # 解析数据帧并打印
        data_frame = np.frombuffer(byte_data_frame, dtype='uint16')
#         print("Received frame:", data_frame, len(data_frame))
        
        ADCPA1 = data_frame[:1000]
        print("PA1:\n",ADCPA1,len(ADCPA1))
        ADCPA0 = data_frame[1000:2000]
        print("PA0:\n",ADCPA0,len(ADCPA0))
except KeyboardInterrupt:
    # 在Ctrl+C中断程序时关闭串口
    ser.close()
