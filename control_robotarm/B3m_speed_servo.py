#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time

class B3M_Ctrl():
    def __init__(self,now_angle):
        #ロボットアームの初期移動
        self.robot_arm = b3mCtrl.B3mClass()
        self.robot_arm.begin("/dev/ttyUSB0",1500000)
        self.now_anlge = now_angle
        self.diff_angle = [-3.0, 3.0] #精度
        self.idx = [2,1,3]

    def go_target_anlge(self,target_angle):

        #モード設定
        for id in range(len(self.idx)):
            print(aaa.setMode(self.idx[id],"FREE"))
            time.sleep(0.01)
            print(aaa.setMode(self.idx[id],"SPEED"))
            time.sleep(0.01)

            hoge = aaa.setRam(self.idx[id], 0, "DesiredVelosity")
            time.sleep(0.01)

            hoge = aaa.setRam(self.idx[id], 0, "EncoderCount")
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
                    if target_angle[id]+diff_angle[0] <= now_angle[id] and now_angle[id]<= target_angle[id]+diff_angle[1]:
                        hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
                        time.sleep(0.01)
                        counter += 1

                    elif now_angle[id] < target_angle[id]:
                        hoge = aaa.setRam(idx[id], 10000, "DesiredVelosity")
                        time.sleep(0.01)
                    elif now_angle[id] > target_angle[id]:
                        hoge = aaa.setRam(idx[id], -10000, "DesiredVelosity")
                        time.sleep(0.01)
                        pass
            if counter == len(idx): #すべての速度が0
                break

            #エンコーダを読み込み
            for id in range(len(idx)):
                run = 1
                print("read id : ",idx[id])
                while run==1:
                    hoge = aaa.getRam(idx[id],"EncoderCount")
                    if(hoge[0] != False):
                        now_angle[id] = hoge[0]*360.0/61440.0
                        print("now_angle")
                        print(now_angle[id])
                        run=0
                    time.sleep(0.01)

