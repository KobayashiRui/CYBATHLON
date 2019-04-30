import os 
import sys
import time
import serial

#control_motorディレクトリへのパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '../control_motor'))

import blv_lib
import az_lib_direct

#自分の端末ごとに適切に設定する
client = serial.Serial("/dev/ttyXRUSB0",115200,timeout=0.1,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)
#右クローラ
motor1 = blv_lib.blv_motor(client,1) 
#左のクローラ
motor2 = blv_lib.blv_motor(client,2) 

#右クローラと左クローラに速度を設定######
#motor1.set_speed(100)
motor2.set_speed(100)
##########################################

print("go")
#右クローラと左クローラを回転させる######
#motor1.go(0,1)#fw,rev
#motor2.go(1,0)
motor2.go(0,1)
#########################################

#十秒回転
print("start 10 second")
time.sleep(1)
print("end")

#右クローラと左クローラに速度を設定######
#motor1.set_speed(0)
motor2.set_speed(0)
##########################################

#右クローラと左クローラを回転させる######
#motor1.go(0,0)#fw,rev
motor2.go(0,0)
#########################################

print("end")
