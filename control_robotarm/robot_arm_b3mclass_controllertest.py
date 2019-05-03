import numpy as np
import B3m_speed_servo_lib
import usb.core
import usb.util
import sys
from time import gmtime, strftime
import time
import copy
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

DED_ZONE = 120
Z_DED_ZONE = 250
DIFF_SIZE = 5
Z_DIFF_SIZE = 10

dev = usb.core.find(idVendor=0x46d, idProduct=0xc626)
if dev is None:
    raise ValueError('SpaceNavigator not found');
else:
    print('SpaceNavigator found')
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

#ロボットアームの初期設定#####################################
my_chain = Chain.from_urdf_file("cybathlon_robotarm.URDF")
Now_pos = my_chain.forward_kinematics([0]*4)[:,3][0:3] #展開後の初期姿勢を設定
##############################################################
#B3M(ロボットアーム展開)######################################
my_chain_b3m = B3m_speed_servo_lib.B3M_class()
#my_chain_b3m.start_arm()
##############################################################

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
                #アームの目標地点の設定
                #アームの角度を求める
                #目標角度へ移動

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
                #アームの地点の設定・更新(最大で1cm追加)
                Now_pos[1] += R_list[0]/3500
                Now_pos[0] -= R_list[1]/3500
                #4*4行列を算出
                Target_pos = np.eye(4)
                Target_pos[0][3] = Now_pos[0]
                Target_pos[1][3] = Now_pos[1]
                Target_pos[2][3] = Now_pos[2]
                #アームの角度を求める
                target_angle = my_chain.inverse_kinematics(Target_pos)
                #目標角度へ移動
                #go_target_angle
                my_chain_b3m.go_target_angle(np.rad2deg(target_angle[0:3]))

        #ボタンの判定(左が2,右が1,同時押しが3)
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
