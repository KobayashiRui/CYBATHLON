import usb.core
import usb.util
import os 
import sys
from time import gmtime, strftime
import time
import copy
import serial

#control_motorディレクトリへのパを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '../control_motor'))

import blv_lib
import az_lib_direct

#自分の端末ごとに適切に設定する
client = serial.Serial("/dev/ttyXRUSB0",115200,timeout=0.1,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)

motor3 = az_lib_direct.az_motor_direct(client,3) 

print("move 0")
motor3.go(0)

input()

print("move lift up")
motor3.go(17200)

input()

print("move 0")
motor3.go(0)
input()

print("move torque")
motor3.go_torque(150)

input()

print("move 0")
motor3.go(0)

input()

print("end")