# main.py -- put your code here!
import pyb
import micropython
import machine
from pyb import Pin
from pyb import ADC
from pyb import DAC
from pyb import USB_VCP
from pyb import Timer
from array import array
import math
micropython.alloc_emergency_exception_buf(50)
led1 = pyb.LED(1)
led2 = pyb.LED(2)
#'usb' RENAMED USB_VCP OBJECT
usb=USB_VCP()

#ADC intialization
#Buffersize define
from array import array
BUFFERSIZE=1000
#ADC@PA1 PA0 Max input Frequency:10kHz
adc1 = ADC('PA1') # pin input = PA1
adc0 = ADC('PA0') # pin input = PA0
adc_buf1=array('H',(0 for i in range(BUFFERSIZE)))
adc_buf0=array('H',(0 for i in range(BUFFERSIZE))) 
sample_frequency = 50000
adc_samp=Timer(9,freq=sample_frequency)

#DAC@PA4 PA5
PA4 = machine.Pin('PA4', machine.Pin.OUT)
PA5 = machine.Pin('PA5',machine.Pin.OUT)
dac5 = pyb.DAC(PA5)
dac4 = pyb.DAC(PA4)
dac4.triangle(8192000)
dac5.write(0)


# 定义握手信号
START_SIGNAL = 'SSTART\n'
CONFIRM_SIGNAL = 'ACKACK\n'
FINISH_SIGNAL = 'FINISH\n'

while True:

        
    if usb.any():
        data = usb.read(25)
        cmd = data.decode('utf-8')
#         cmd =START_SIGNAL
#     # 读取开始信号
# #     start_signal = 'SSTART\n'
        if cmd[0:2] == 'SS':
            # 发送确认信号
            usb.write(CONFIRM_SIGNAL)
#             usb.write('this is data\n')
            ADC.read_timed_multi((adc1,adc0),(adc_buf1,adc_buf0),adc_samp)
            usb.write(adc_buf1)
            usb.write(adc_buf0)
#             

#         else:
# #             #没有开始信号就什么也不做
# #             led1.off()
# #             led2.off()
#             continue
