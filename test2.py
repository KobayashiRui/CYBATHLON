import serial
client = serial.Serial("/dev/ttyXRUSB0", 9600, timeout=0.01, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

size= 16
print(client.name)
commando=b"\x01\x03\x04\x80\x00\x04\x44\xD1"
client.write(commando)
result = client.read(size)
print(result)
print("fin")

