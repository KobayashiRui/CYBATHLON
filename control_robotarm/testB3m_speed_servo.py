#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time



if __name__ == '__main__':
    aaa = b3mCtrl.B3mClass()
    aaa.begin("/dev/ttyUSB0",1500000)
    #now_angle = [0,0,0]
    now_angle = [0,0,0]
    target_angle = [-5,-5,-5]
    diff_angle = [-3,3]
    
    idx= [2,1,3]
    for id in range(len(idx)):
        print(aaa.setMode(idx[id],"FREE"))
        time.sleep(0.01)
        #print(aaa.setTrajectoryType(id,"EVEN"))
        #print(aaa.setTrajectoryType(id,"NORMAL"))
        print(aaa.setMode(idx[id],"SPEED"))
        time.sleep(0.01)
        
        hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
        time.sleep(0.01)
        
        hoge = aaa.setRam(idx[id], 0, "EncoderCount")
        time.sleep(0.01)

        
        print("read")
        run = 1
        for id in range(len(idx)):
            while run==1:
                hoge = aaa.getRam(idx[id],"EncoderCount")
                if(hoge[0] != False):
                    now_angle[id] = hoge[0]*360.0/61440.0
                    print("now_angle")
                    print(now_angle[id])
                    run=0
                time.sleep(0.01)

        if(hoge is not False):
    	    print(idx[id])
    
    #full motor go
    print("go")
    for i in range(1000):

        for id in range(len(idx)):
                if target_angle[id]+diff_angle[0] <= now_angle[id] and now_angle[id]<= target_angle[id]+diff_angle[1]:
                    hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
                    time.sleep(0.01)

                elif now_angle[id] < target_angle[id]:
                    hoge = aaa.setRam(idx[id], 10000, "DesiredVelosity")
                    time.sleep(0.01)
                elif now_angle[id] > target_angle[id]:
                    hoge = aaa.setRam(idx[id], -10000, "DesiredVelosity")
                    time.sleep(0.01)
                    pass
                
        #full motor read
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

    for id in range(len(idx)):
            hoge = aaa.setRam(idx[id], 0, "DesiredVelosity")
