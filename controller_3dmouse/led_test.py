import RPi.GPIO as IO
import time
#x : 12,16,18,22
#y : 7,11,13,15
X_list = [7,11,13,15]
Y_list = [12,16,18,22]
GPIO = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
flag = 0
while 1:
    for y range(len(GPIO)):
        for x range(len(GPIO[x])):
            if GPIO[x][y] == 1:
                #off
                IO.output(X_list[x],1)
                IO.output(Y_list[y],0)
                time.sleep(0.001)
                #on
                IO.output(X_list[x],0)
                IO.output(Y_list[y],1)
                time.sleep(0.001)




