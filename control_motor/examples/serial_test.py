import serial
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import crc16
#off/off/on
client = serial.Serial("/dev/ttyACM0", 115200, timeout=10, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

size= 16

#速度設定
commando=b"\x01\x10\x04\x80\x00\02\x04\x00\x00\x0F\xA0"
print(commando)
result = crc16.calc_crc16(commando)
print("result")
print(commando + result)
commando = commando + result
client.write(commando)
result = client.read()
print(result)

#回転開始
commando=b"\x01\x10\x00\x7C\x00\02\x04\x00\x00\x00\x28"
print(commando)
result = crc16.calc_crc16(commando)
print("result")
print(commando + result)
commando = commando + result
client.write(commando)
result = client.read()
print(result)

print("fin")
