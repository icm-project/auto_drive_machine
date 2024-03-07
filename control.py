#!/usr/bin/env python
# coding: utf-8

# In[1]:


import serial
import time

try:
    ser = serial.Serial(
        port='\\\\.\\COM7',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
    )
    print("Serial Port Connected ")
except:
    print("Please Check COM Port !!!")
def start(ser):
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()
    ser.write(('\x1B\x64\x05ACI#0450#0450#E\r\n').encode("utf-8"))
    ser.close()
    print("Start Sign Detected")

    
def stop(ser):
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()
    ser.write(('\x1B\x64\x05ACI#0000#0000#E\r\n').encode("utf-8"))
    ser.close()
    print("Stop Sign Detected")

    
def slow_down(ser):
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()
    ser.write(('\x1B\x64\x05ACI#0420#0420#E\r\n').encode("utf-8"))
    ser.close()
    print("Slow Down Sign Detected")

    
def speed_up(ser):
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()
    ser.write(('\x1B\x64\x05ACI#0510#0510#E\r\n').encode("utf-8"))
    ser.close()
    print("Speed Up Down Sign Detected")

    
def limited_stop(ser):
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()
    ser.write(('\x1B\x64\x05ACI#0000#0000#E\r\n').encode("utf-8"))
    ser.close()
    print("Limited Stop Down Sign Detected")
    time.sleep(10)
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()
    ser.write(('\x1B\x64\x05ACI#0450#0450#E\r\n').encode("utf-8"))
    ser.close()
    
def force_start(ser):
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()
    ser.write(('\x1B\x64\x05ACI#0450#0450#E\r\n').encode("utf-8"))
    ser.close()

    


# In[2]:


ser.close()


# In[ ]:




