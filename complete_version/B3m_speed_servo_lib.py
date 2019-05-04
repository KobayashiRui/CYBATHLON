#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time

class B3M_class():
    def __init__(self):
        #ロボットアームの初期移動
        self.robot_arm = b3mCtrl.B3mClass()
        self.robot_arm.begin("/dev/ttyUSB0",1500000)
        self.now_angle = [0,0,0]
        self.diff_angle = [-2.0, 2.0] #精度
        self.idx = [2,1,3]
    
    def set_origin(self):
        self.go_target_angle([0,0,0])

    def start_arm(self):
        self.go_target_angle([180,-30,-100])

        #エンコードカウントを0に設定
        for id in range(len(self.idx)):
            hoge = self.robot_arm.setRam(self.idx[id], 0, "EncoderCount")
            time.sleep(0.01)
        self.now_angle = [0,0,0]

    def go_pos(self,id_number,target_angle):
        self.robot_arm.TrajectoryType(id_number,"EVEN")
        self.robot_arm.setMode(id_number,"POSITION")
        self.robot_arm.positionCmd(target_angle)

    def go_target_angle(self,target_angle):

        #モード設定
        for id in range(len(self.idx)):
            print(self.robot_arm.setMode(self.idx[id],"FREE"))
            time.sleep(0.01)
            print(self.robot_arm.setMode(self.idx[id],"SPEED"))
            time.sleep(0.01)

            hoge = self.robot_arm.setRam(self.idx[id], 0, "DesiredVelosity")
            time.sleep(0.01)



            #run = 1
            #for id in range(len(self.idx)):
            #    while run==1:
            #        hoge = aaa.getRam(self.idx[id],"EncoderCount")
            #        if(hoge[0] != False):
            #            now_angle[id] = hoge[0]*360.0/61440.0
            #            print("now_angle")
            #            print(now_angle[id])
            #            run=0
            #        time.sleep(0.01)
    
        #位置制御
        while True:
            #位置回転方向のセット
            counter = 0
            for id in range(len(self.idx)):
                    if target_angle[id]+self.diff_angle[0] <= self.now_angle[id] and self.now_angle[id]<= target_angle[id]+self.diff_angle[1]:
                        hoge = self.robot_arm.setRam(self.idx[id], 0, "DesiredVelosity")
                        time.sleep(0.01)
                        counter += 1

                    elif self.now_angle[id] < target_angle[id]:
                        hoge = self.robot_arm.setRam(self.idx[id], 10000, "DesiredVelosity")
                        time.sleep(0.01)
                    elif self.now_angle[id] > target_angle[id]:
                        hoge = self.robot_arm.setRam(self.idx[id], -10000, "DesiredVelosity")
                        time.sleep(0.01)
                        pass
            if counter == len(self.idx): #すべての速度が0
                break

            #エンコーダを読み込み
            for id in range(len(self.idx)):
                run = 1
                print("read id : ",self.idx[id])
                while run==1:
                    hoge = self.robot_arm.getRam(self.idx[id],"EncoderCount")
                    if(hoge[0] != False):
                        self.now_angle[id] = hoge[0]*360.0/61440.0
                        print("now_angle")
                        print(self.now_angle[id])
                        run=0
                    time.sleep(0.01)

        return 1
