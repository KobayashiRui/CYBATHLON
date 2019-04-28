import serial
import crc16
import time

#off/off/on
client = serial.Serial("/dev/ttyXRUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

size= 16

#速度設定
commando=b"\x01\x10\x04\x80\x00\02\x04\x00\x00\x0F\xA0"
print(commando)
result = crc16.calc_crc16(commando)
print(commando + result)
commando = commando + result
client.write(commando)
result = client.read()
input()

#回転開始
commando=b"\x01\x10\x00\x7C\x00\02\x04\x00\x00\x00\x28"
print(commando)
result = crc16.calc_crc16(commando)
print(commando + result)
commando = commando + result
client.write(commando)

print("fin")