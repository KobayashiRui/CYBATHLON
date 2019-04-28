#azライブラリの動作確認プログラム

import serial
import az_lib_direct
import time

client = serial.Serial("/dev/ttyXRUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

motor1 = az_lib_direct.az_motor_direct(client,1,[0,58436,116750])
print("go list 1")
motor1.go_list(1)
time.sleep(5)
print("go list 0")
motor1.go_list(0)
time.sleep(5)
print("fin")
