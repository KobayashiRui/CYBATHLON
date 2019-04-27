from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

#parityのE??
client = ModbusClient(method = "rtu", port="",stopbits=1,bytesize=8,parity='E',baudrate=115200,timeout=0.02)
connection = client.connect()

#書き込みメッセージ作成
builder = BinaryPayloadBuilder(byteorder=Endian.Big)#Endian big1?
builder.add_32bit_int()#代入したい数値
result = client.write_registers(address=,values=builder.build(),unit=,skip_encode=True)
#address : 囲みたいレジスタの最初のアドレス
#unit : 送信相手のID
