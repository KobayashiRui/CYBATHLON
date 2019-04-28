from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
import time

#parityのE??
client = ModbusClient(method = "rtu", port="/dev/ttyXRUSB0",stopbits=1,bytesize=8,parity='E',baudrate=9600,timeout=0.01)
connection = client.connect()
print(connection)


#FW方向回転開始
print("start fw")
#################################################################################################################
#回転速度(No.0)の設定
builder = BinaryPayloadBuilder(byteorder=Endian.Little)#Endian big1?
builder.add_32bit_int(1000)#代入したい数値(10進数)#200r/min
result = client.write_registers(address=0x0480,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#address : 囲みたいレジスタの最初のアドレス
#unit : 送信相手のID

#回転開始
builder = BinaryPayloadBuilder(byteorder=Endian.Big)
builder.add_32bit_int(0b00101000)#代入したい数値(10進数)#0x007C : 0b00000000,00000000 0x007D : 0b00000000,00101000
result = client.write_registers(address=0x007C,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#################################################################################################################

#3秒待機
time.sleep(10)


#回転停止命令
print("start stop")
#################################################################################################################
#回転速度(No.0)の設定
builder = BinaryPayloadBuilder(byteorder=Endian.Big)#Endian big1?
builder.add_32bit_int(0)#代入したい数値(10進数)#200r/min
result = client.write_registers(address=0x0480,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#address : 囲みたいレジスタの最初のアドレス
#unit : 送信相手のID

#回転停止
builder = BinaryPayloadBuilder(byteorder=Endian.Big)
builder.add_32bit_int(0b00100000)#代入したい数値(10進数)#0x007C : 0b00000000,00000000 0x007D : 0b00000000,00101000
result = client.write_registers(address=0x007C,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#################################################################################################################

#3秒待機
time.sleep(3)


#REV方向回転開始
print("start rev")
#################################################################################################################
#回転速度(No.0)の設定
builder = BinaryPayloadBuilder(byteorder=Endian.Big)#Endian big1?
builder.add_32bit_int(1000)#代入したい数値(10進数)#200r/min
result = client.write_registers(address=0x0480,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#address : 囲みたいレジスタの最初のアドレス
#unit : 送信相手のID

#回転開始
builder = BinaryPayloadBuilder(byteorder=Endian.Big)
builder.add_32bit_int(0b00110000)#代入したい数値(10進数)#0x007C : 0b00000000,00000000 0x007D : 0b00000000,00101000
result = client.write_registers(address=0x007C,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#################################################################################################################

#3秒待機
time.sleep(3)

#回転停止命令
print("start stop")
#################################################################################################################
#回転速度(No.0)の設定
builder = BinaryPayloadBuilder(byteorder=Endian.Big)#Endian big1?
builder.add_32bit_int(0)#代入したい数値(10進数)#200r/min
result = client.write_registers(address=0x0480,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#address : 囲みたいレジスタの最初のアドレス
#unit : 送信相手のID

#回転停止
builder = BinaryPayloadBuilder(byteorder=Endian.Big)
builder.add_32bit_int(0b00100000)#代入したい数値(10進数)#0x007C : 0b00000000,00000000 0x007D : 0b00000000,00101000
result = client.write_registers(address=0x007C,values=builder.build(),unit=0x01,skip_encode=True)
print(result)
#################################################################################################################

print("fin!!")