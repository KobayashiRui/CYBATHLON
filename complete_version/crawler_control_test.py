import usb.core
import usb.util
import os 
import sys
from time import gmtime, strftime
import time
import copy
import serial

#control_motorディレクトリへのパを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '../control_motor'))

import blv_lib
import az_lib_direct

#自分の端末ごとに適切に設定する
client = serial.Serial("/dev/ttyXRUSB0",115200,timeout=0.1,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)

#右クローラ
motor1 = blv_lib.blv_motor(client,1) 
#左のクローラ
motor2 = blv_lib.blv_motor(client,2) 

DED_ZONE = 150
Z_DED_ZONE = 250
DIFF_SIZE = 10
Z_DIFF_SIZE = 10

dev = usb.core.find(idVendor=0x46d, idProduct=0xc626)
if dev is None:
    raise ValueError('SpaceNavigator not found');
else:
    print(dev)

cfg = dev.get_active_configuration()
print('cfg is ', cfg)
intf = cfg[(0,0)]
print('intf is ', intf)
ep = usb.util.find_descriptor(intf, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
print('ep is ', ep)

reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

ep_in = dev[0][(0,0)][0]
ep_out = dev[0][(0,0)][1]

print('')
print('Exit by pressing any button on the SpaceNavigator')
print('')

Z_push = 0
old_Z_push = 0

R_list = [0,0,0]
old_R_list = 0

Button_number = 0


run = True
while run:
    try:
        data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)

        #Z軸のプッシュ判定
        if data[0] == 1:
            old_Z_push = copy.deepcopy(Z_push)
            Z_push = data[5] + (data[6]*256)

            if data[6] > 127:
                Z_push -= 65536

            #デッドゾーンの処理
            if Z_push <= Z_DED_ZONE and Z_push >= -Z_DED_ZONE:
                Z_push = 0

            #感度の処理
            diff = abs(Z_push - old_Z_push)
            if diff > Z_DIFF_SIZE and sum(R_list) == 0:
                print("Push: ",Z_push)

        #回転の移動判定
        if data[0] == 2:
            old_R_list = copy.deepcopy(R_list)
            R_list[0] = data[1] + (data[2]*256)
            R_list[1] = data[3] + (data[4]*256)
            R_list[2] = data[5] + (data[6]*256)
            
            if data[2] > 127:
                R_list[0] -= 65536
            if data[4] > 127:
                R_list[1] -= 65536
            if data[6] > 127:
                R_list[2] -= 65536

            #デッドゾーンの処理
            for i in range(3):
                if R_list[i] <= DED_ZONE and R_list[i] >= -DED_ZONE :
                    R_list[i] = 0

            #感度の処理
            diff = abs(sum(R_list) - sum(old_R_list))
            if diff > DIFF_SIZE and abs(Z_push) < Z_DED_ZONE:
                print("R: ", R_list[0], R_list[1], R_list[2])
                #回転の処理
                if R_list[0] == 0:
                    motor1.set_speed(0)
                    motor2.set_speed(0)
                    motor1.go(0,0)
                    motor2.go(0,0)
                elif R_list[0] > 0:
                    #回転速度を設定する
                    motor1.set_speed(int(abs(80*R_list[0]*0.01)))
                    motor2.set_speed(int(abs(80*R_list[0]*0.01)))
                    motor1.go(0,1)
                    motor2.go(1,0)
                elif R_list[0] < 0: 
                    motor1.set_speed(int(abs(80*R_list[0]*0.01)))
                    motor2.set_speed(int(abs(80*R_list[0]*0.01)))
                    motor1.go(1,0)
                    motor2.go(0,1)

        #ボタンの判定(左が2,右が1)
        if data[0] == 3:
            if data[1]== 0:
                print("push button : ", Button_number)
                Button_number = 0
            else:
                Button_number = data[1]

    except KeyboardInterrupt:
        print("end")
        break

    except usb.core.USBError:
        print("USB error")
    

# end while
usb.util.dispose_resources(dev)

if reattach:
    dev.attach_kernel_driver(0)
