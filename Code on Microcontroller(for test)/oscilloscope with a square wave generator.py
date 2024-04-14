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
# 定义LED灯连接的引脚
led1 = pyb.LED(1)
led2 = pyb.LED(2)
#'usb' RENAMED USB_VCP OBJECT
usb=USB_VCP()

# 定义PA4输出引脚
PA4 = machine.Pin('PA4', machine.Pin.OUT)
#创建DAC对象
dac = pyb.DAC(PA4)


def agen(ch,freq,typ,amp,os,ns): #os目标电压值中线   amp 目标电压摆动
    dac=DAC(ch,bits=12,buffering=True)  # DAC output: ch1 at pin PA4 and ch2 at pin PA5 选引脚，设置分辨率，设置缓冲
    if amp==0:
       dac.write(int((4095/3.3)*os))   #12bits 4096 参考电压3.3V 电压值转换成DAC值
    else:
        if typ=='sin':
           buf=array('H',(int((4095/3.3)*(os+amp*math.sin(2*math.pi*i/ns)))) for i in range(ns))
        elif typ=='cos':
           buf=array('H',(int((4095/3.3)*(os+amp*math.cos(2*math.pi*i/ns)))) for i in range(ns)) 
        elif typ=='tri':
           k=int(ns/2)
           buf=array('H',(int((4095/3.3)*(os+amp*(4.0*i/ns-1.0)))) for i in range(k)) 
           buft=array('H',(int((4095/3.3)*(os+amp*(3.0-4.0*i/ns)))) for i in range(k,ns))
           buf=buf+buft  
        dac.write_timed(buf,Timer(5+ch,freq=freq*len(buf)),mode=DAC.CIRCULAR)
# Initialize waveform generators output
w1_gain=11
w1_dc=1.65
w2_gain=11
w2_dc=1.65
freq1=1000
freq2=1000
wtype1='sin'
wtype2='sin'
amp1=0
amp2=0
os1=w1_dc
os2=w2_dc
ns1=64
ns2=64
agen(1,freq1,'sin',amp1,os1,ns1)
agen(2,freq2,'sin',amp2,os2,ns2)

################Code for test PLEASE DELETE IT#######################
#DAC@PA4 PA5
PA4 = machine.Pin('PA4', machine.Pin.OUT)
PA5 = machine.Pin('PA5',machine.Pin.OUT)
dac5 = pyb.DAC(PA5)
dac4 = pyb.DAC(PA4)
dac5.triangle(8192000)
dac4.write(0)
#ADC CODE #########################################################
#######################Sqaure Wave################################
pwm_pin = pyb.Pin('PB0', pyb.Pin.OUT)
trigger_frequency = 1000
pwm_pin.value(0)
def toggle_pin(timer):
    pwm_pin.value(not pwm_pin.value())  # 方波产生函数
tim = pyb.Timer(8, freq=trigger_frequency)  # 使用定时器 8，设置频率
tim.callback(toggle_pin)  # 设置定时器中断回调函数
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


# 定义握手信号
START_SIGNAL = 'SSTART\n'
CONFIRM_SIGNAL = 'ACKACK\n'
FINISH_SIGNAL = 'FINISH\n'
##########################################################


while True:
 if usb.any():
    data=usb.read(25)
    mode=data.decode('utf-8')
    #mode = input()
    if (mode[0:2]=='s1'):
        led1.on()
        time.sleep(1)  # 等待1秒
        led1.off()
        wnum1=int(mode[2:4]) #选波形
        ns1=int(mode[4:7])   #选ns波形周期
        freq1=int(mode[7:14]) #选freq采样频率
        amp11=(int(mode[14:18])) #放大倍数
        amp1= amp11 / 10
  #      amp1=amp1/w1_gain  #考虑硬件放大电路倍数
        os11=(int(mode[18:22])) # os目标电压值DC中线
        os1=os11 / 10 # os目标电压值DC中线
   #     os1=os1/w1_gain+w1_dc  #考虑硬件放大电路电压补偿
        if wnum1==0:
            wtype1='sin'
        elif wnum1==1:
           wtype1='cos'
        elif wnum1==10:
             wtype1='tri'
        else:
             wtype1='none'
        print(wnum1,ns1,freq1,amp1,os1)
        agen(1,freq1,wtype1,amp1,os1,ns1) #output at PA4
        agen(2,freq2,wtype2,amp2,os2,ns2) #output at PA5  # reduce the occurrence of 
    if (mode[0:2]=='s2'):
        led2.on()
        time.sleep(1)  # 等待1秒
        led2.off()
        wnum2=int(mode[2:4])
        ns2=int(mode[4:7])
        freq2=int(mode[7:14])
        amp21=(int(mode[14:18]))
        amp2=amp21 / 10
  #      amp2=amp2/w2_gain 
        os21=(int(mode[18:]))
        os2=os21/10
  #      os2=os2/w2_gain+w2_dc
        if wnum2==0:
            wtype2='sin'
        elif wnum2==1:
            wtype2='cos'
        elif wnum2==10:
            wtype2='tri'
        else:
            wtype2='none'
        agen(2,freq2,wtype2,amp2,os2,ns2) #output at PA5
        agen(1,freq1,wtype1,amp1,os1,ns1) #output at PA4 # reduce the occurrence of
        
###############################ADC######################

    if mode[0:2] == 'SS':
        # 发送确认信号
        usb.write(CONFIRM_SIGNAL)
        ADC.read_timed_multi((adc1,adc0),(adc_buf1,adc_buf0),adc_samp)
        usb.write(adc_buf1)
        usb.write(adc_buf0)



