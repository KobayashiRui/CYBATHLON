#!/usr/bin/env python
#coding: utf-8

import b3mCtrl
import time



if __name__ == '__main__':
    aaa = b3mCtrl.B3mClass()
    aaa.begin("/dev/ttyUSB0",115200)
    
    idx= [2,1,3]

    for id in idx:
        run =1
        while run:
            hoge = aaa.getRam(id,"EncoderCount")
            if(hoge[0] != False):
                print(id)
                print(hoge[0])
                run=0
            if(hoge is not False):
                #print(id)
                pass
