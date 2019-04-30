import serial

client = serial.Serial("/dev/ttyAMA0",115200,timeout=0.1,bytesize=8,parity=serial.NONE,stopbits=serial.STOPBITS_ONE)

command = b"\x05\x01\x00\x01\x07"
client.write()
result = client.read()
print(result)