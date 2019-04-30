import serial
import b3m_sender

client = serial.Serial("/dev/ttyUSB0",115200,timeout=0.1,bytesize=8,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
test1 = b3m_sender.b3m(client,[1])
test1.set_speed_control_mode()
test1.send_speed_list([100])
