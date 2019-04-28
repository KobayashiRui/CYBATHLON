import blv_lib
import time

client = serial.Serial("/dev/ttyXRUSB0", 115200, timeout=0.1, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE) # COMポートは自分の奴を入れる

motor1 = blv_lib.blv_motor(client,1)
motor1.set_speed_and_go(100,1,0)

time.sleep(3)

motor1.set_speed_and_go(0,1,0)
