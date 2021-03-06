import RPi.GPIO as GPIO
import numpy as np
import usb.core
import usb.util
import os 
import sys
from time import gmtime, strftime
import time
import copy
import serial
import B3m_speed_servo_lib
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

#control_motorディレクトリへのパを追加
sys.path.append(os.path.join(os.path.dirname(__file__), '../control_motor'))
import blv_lib
import az_lib_direct

#GPIO_init###########################################
pin_list = [12,16,18] #move,rclu,arm
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_list[0],GPIO.OUT)
GPIO.setup(pin_list[1],GPIO.OUT)
GPIO.setup(pin_list[2],GPIO.OUT)
#####################################################

#定数################################################
DED_ZONE = 150
Z_DED_ZONE = 250
DIFF_SIZE = 1
Z_DIFF_SIZE = 10
#####################################################


#状態変数############################################
Mode = 0 #0:クローラ, 1:リモートセンタ機構&リフトアップ, 2:ロボットアーム
RC_mode = 1 #0:階段降り, 1:真ん中, 2:椅子座り, 3:階段上り
LU_mode = 1 #0:収納, 1:テンション維持モード 2:リフトアップ
ARM_flag = 0
#####################################################

#LED#################################################
def LED_setting(pin_data_list):
    global pin_list
    for i in range(len(pin_list)):
        GPIO.output(pin_list[i],pin_data_list[i])
#####################################################

#ロボットアームアームの初期位置を設定################
my_chain = Chain.from_urdf_file("cybathlon_robotarm.URDF")
#展開後の姿勢データから位置データを算出
Now_pos = my_chain.forward_kinematics([0]*4)[:,3][0:3]
#####################################################

#B3M#################################################
my_chain_b3m = B3m_speed_servo_lib.B3M_class()
my_chain_b3m.set_origin()
my_chain_b3m.go_pos(4,0)#手首の位置を設定
b3m_target_angle = 0
#####################################################

#リミッター関連######################################
#ロボットアームの位置制御
X_MAX_limit = 1.3 #1m30まで
X_MIN_limit = 0.5  
Y_MAX_limit = 3
Y_MIN_limit = -3
Z_MAX_limit = 3
Z_MIN_limit = -3
#手首の制限
Angle_MAX = 3100
Angle_MIN = -3100
#####################################################

#サーフティーの状態
Safety = 0

while True:
    #セーフティの読み込み
    Safety = 1 #ここで確定1だが実際はボタンの値を読み込む
    if Safety == 0:
        continue

    #コントローラ変数(セーフティ解除時に初期化される)#######
    Z_push = 0          #Z軸方向の変位
    old_Z_push = 0      #前回のZ軸方向の変位
    R_list = [0,0,0]    #軸に対する回転の変位
    old_R_list = 0      #前回の軸に対する回転の変位
    Button_number = 0   #左右のボタンの値
    ########################################################

    #RC変数#################################################
    RC_flag = 1         #クリックの判定(1の時は次への移動をしない)
    ########################################################
    #LED_setting############################################
    LED_setting([1,0,0]) 
    ########################################################

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


    #自分の端末ごとに適切に設定する
    client = serial.Serial("/dev/ttyXRUSB0",115200,timeout=0.1,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)
    #モータのインスタンス化##############################
    motor1 = blv_lib.blv_motor(client,1) #右クローラ
    motor2 = blv_lib.blv_motor(client,2) #左のクローラ
    motor3 = az_lib_direct.az_motor_direct(client,3) #リフトアップ右
    motor4 = az_lib_direct.az_motor_direct(client,4) #リフトアップ左
    motor5 = az_lib_direct.az_motor_direct(client,5,[0,58436,90000,116750]) #リモートセンタ
    #####################################################

    #初期移動ステッピングモータ関連######################
    #リモートセンターの移動
    motor5.go_list(RC_mode)
    #リフトアップの移動
    if LU_mode == 0:
        motor3.go(0)
        motor4.go(0)
    elif LU_mode == 1:
        motor3.go_torque(300)#15%
        motor4.go_torque(300)#15%
    elif LU_mode == 2:
        motor3.go(13200)#位置移動
        motor4.go(13200)#位置移動
    #####################################################

    #初期設定ブラシレスモータ関連########################
    motor1.set_acc_dec_time(2)
    motor2.set_acc_dec_time(2)
    #####################################################



    while True:
        try:
            data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)

            #Z軸のプッシュ判定#############################################################
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

                    #Mode:0 クローラモード
                    if Mode == 0:
                        pass
                    #Mode:1 リモート&リフトアップ 
                    elif Mode == 1:
                        if Z_push > 300:
                            LU_mode = 2
                            motor5.go_list(3)
                            time.sleep(5)
                            motor3.go(point=13200,speed=200,rate=1)
                            motor4.go(point=13200,speed=200,rate=1)
                            motor5.go_list(RC_mode)
                            
                        elif Z_push < -250:
                            LU_mode = 0
                            motor3.go(point=0)
                            motor4.go(point=0)

                    #Mode2 : アームモード
                    elif Mode == 2 and ARM_flag == 1:
                        if Z_MIN_limit <= (Now_pos[2] - Z_push/3500)  and (Now_pos[2] - Z_push/3500) <= Z_MAX_limit :
                            #アームの目標地点の設定
                            Now_pos[2] -= Z_push/3500
                            #4*4行列を算出
                            Target_pos = np.eye(4)
                            Target_pos[0][3] = Now_pos[0]
                            Target_pos[1][3] = Now_pos[1]
                            Target_pos[2][3] = Now_pos[2]
                            #アームの角度を求める
                            target_angle = my_chain.inverse_kinematics(Target_pos)
                            #目標角度へ移動
                            #go_target_angle
                            print("go arm")
                            result = my_chain_b3m.go_target_angle(np.rad2deg(target_angle[0:3]))
            ##############################################################################

            #Rの移動判定##################################################################
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

                    #Mode:0 クローラモード
                    if Mode == 0:
                        if R_list[0] == 0 and R_list[1] == 0 and R_list[2]==0: #停止
                            #motor1.set_speed(0)
                            #motor2.set_speed(0)
                            motor1.go(1,1)
                            motor2.go(1,1)
                        elif R_list[0] > 0: #前進移動
                            if R_list[1] >= 0:#左をはやく
                                motor1.set_speed(int(abs(80*R_list[0]*0.01)))
                                motor2.set_speed(int(abs(80*R_list[0]*0.01)) + int(R_list[2]*0.04))
                            elif R_list[0] < 0:#右をはやく
                                motor1.set_speed(int(abs(80*R_list[0]*0.01)) + int(R_list[2]*0.04))
                                motor2.set_speed(int(abs(80*R_list[0]*0.01)))
                            #motor1.go(1,0)
                            #motor2.go(0,1)
                            motor1.go(0,1)
                            motor2.go(1,0)
                        elif R_list[0] < 0:  #後進移動
                            if R_list[1] >= 0:#左をはやく
                                motor1.set_speed(int(abs(80*R_list[0]*0.01)))
                                motor2.set_speed(int(abs(80*R_list[0]*0.01)) + int(abs(R_list[2]*0.04)))
                            elif R_list[1] < 0:#右をはやく
                                motor1.set_speed(int(abs(80*R_list[0]*0.01)))
                                motor2.set_speed(int(abs(80*R_list[0]*0.01)) + int(abs(R_list[2]*0.04)))
                            #motor1.go(0,1)
                            #motor2.go(1,0)
                            motor1.go(1,0)
                            motor2.go(0,1)
                        elif R_list[2] > 0: #右は前,左は後ろ
                            motor1.set_speed(int(abs(80*R_list[2]*0.01)))
                            motor2.set_speed(int(abs(80*R_list[2]*0.01)))
                            motor1.go(1,0)
                            motor2.go(1,0)
                            
                        elif R_list[2] < 0: #左は前,右は後ろ
                            motor1.set_speed(int(abs(80*R_list[2]*0.01)))
                            motor2.set_speed(int(abs(80*R_list[2]*0.01)))
                            motor1.go(0,1)
                            motor2.go(0,1)

                    #Mode:1 リモート&リフトアップ
                    elif Mode == 1:
                        #リモートセンターの判定##########################################
                        if R_list[0] == 0 and RC_flag==1:
                            RC_flag = 0
                        elif R_list[0] > 300 and RC_flag==0:#前への移動
                            if RC_mode == 3:
                                pass
                            else:#移動処理
                                RC_mode+=1
                                motor5.go_list(RC_mode)
                            RC_flag = 1
                        elif R_list[0] < -170 and RC_flag==0:#後ろへの移動
                            if RC_mode == 0:
                                pass
                            else:#移動処理
                                RC_mode -=1
                                motor5.go_list(RC_mode)
                            RC_flag = 1
                        ##################################################################

                        #リフトアップの判定###############################################
                        if abs(R_list[2]) > 340:
                            LU_mode = 1
                            #motor3.go_torque(150)
                            #motor4.go_torque(150)
                            motor3.set_position_deviation(30000)
                            motor4.set_position_deviation(30000)
                            motor3.go_torque_pos(point=9000,op_current=150)
                            motor4.go_torque_pos(point=9000,op_current=150)
                        ##################################################################

                    #Mode:2 アームモード
                elif Mode == 2 and ARM_flag == 1:
                    #手首回転
                    if R_list[0] == 0 and R_list[1] ==0 and R_list[2]>250:
                        print("angle1:",b3m_target_angle)
                        if (b3m_target_angle-1000) >= Angle_MIN:
                            b3m_target_angle -= 1000
                            my_chain_b3m.go_pos(4,b3m_target_angle)#手首の位置を設定

                    #手首回転
                    elif R_list[0] == 0 and R_list[1] ==0 and R_list[2]<-250:
                        print("angle2",b3m_target_angle)
                        if (b3m_target_angle+1000) <= Angle_MAX:
                            b3m_target_angle += 1000
                            my_chain_b3m.go_pos(4,b3m_target_angle)#手首の位置を設定

                    elif R_list[0] != 0 or R_list[1] != 0:
                        if X_MIN_limit <= (Now_pos[0] + R_list[0]/3500)  and (Now_pos[0] + R_list[0]/3500) <= X_MAX_limit :
                            Now_pos[0] += R_list[0]/3500
                            #4*4行列を算出
                            Target_pos = np.eye(4)
                            Target_pos[0][3] = Now_pos[0]
                            Target_pos[1][3] = Now_pos[1]
                            Target_pos[2][3] = Now_pos[2]
                            #アームの角度を求める
                            target_angle = my_chain.inverse_kinematics(Target_pos)
                            #目標角度へ移動
                            #go_target_angle
                            print("go arm")
                            result = my_chain_b3m.go_target_angle(np.rad2deg(target_angle[0:3]))
                        if Y_MIN_limit <= (Now_pos[1] - R_list[1]/3500)  and (Now_pos[1] - R_list[1]/3500) <= Y_MAX_limit :
                            Now_pos[1] -= R_list[1]/3500
                            #4*4行列を算出
                            Target_pos = np.eye(4)
                            Target_pos[0][3] = Now_pos[0]
                            Target_pos[1][3] = Now_pos[1]
                            Target_pos[2][3] = Now_pos[2]
                            #アームの角度を求める
                            target_angle = my_chain.inverse_kinematics(Target_pos)
                            #目標角度へ移動
                            #go_target_angle
                            print("go arm")
                            result = my_chain_b3m.go_target_angle(np.rad2deg(target_angle[0:3]))

            ##############################################################################

            #ボタンの判定(左が2,右が1)####################################################
            if data[0] == 3:
                if data[1]== 0:
                    print("push button : ", Button_number)
                    if Button_number == 1:
                        if Mode == 2:
                            Mode = 0
                        else:
                            Mode += 1
                        if Mode == 1:
                            RC_flag = 0
                    elif Button_number == 2:
                        if Mode == 0:
                            Mode = 2
                        else:
                            Mode -= 1
                        if Mode == 1:
                            RC_flag = 0
                    elif Button_number == 3:
                        my_chain_b3m.start_arm()
                        ARM_flag = 1

                    print("Now Mode:",Mode)
                    if Mode == 0:
                        LED_setting([1,0,0])
                    elif Mode == 1:
                        LED_setting([0,1,0])
                    elif Mode == 2:
                        LED_setting([0,0,1])

                    Button_number = 0

                else:
                    Button_number = data[1]
            ##############################################################################

        except KeyboardInterrupt:
            print("end")
            Safety = 0
            break

        except usb.core.USBError:
            print("USB error")
            Safety = 0
            break
        except:
            print("Error")
            Safety = 0
            break


    # end while
    usb.util.dispose_resources(dev)

    if reattach:
        dev.attach_kernel_driver(0)
