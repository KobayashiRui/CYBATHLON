# See http://stackoverflow.com/questions/29345325/raspberry-pyusb-gets-resource-busy#29347455
# Run python2 as root (sudo /usr/bin/python2.7 /home/pi/pythondev/HelloSpaceNavigator.py)
import usb.core
import usb.util
import sys
from time import gmtime, strftime
import time
import copy

DED_ZONE = 150
Z_DED_ZONE = 250
DIFF_SIZE = 10
Z_DIFF_SIZE = 10

# Look for SpaceNavigator
dev = usb.core.find(idVendor=0x46d, idProduct=0xc626)
if dev is None:
    raise ValueError('SpaceNavigator not found');
else:
    print('SpaceNavigator found')
    print(dev)

# Don't need all this but may want it for a full implementation

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

#T_list = [0,0,0]
#old_T_list = [0,0,0]
Z_push = 0
old_Z_push = 0

R_list = [0,0,0]
old_R_list = 0

Button_number = 0


run = True
while run:
    try:
        data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)

        #print(data)
        # raw data
        # print data

        # print it correctly T: x,y,z R: x,y,z

        if data[0] == 1:
            old_Z_push = copy.deepcopy(Z_push)
        #    # translation packet
        #    tx = data[1] + (data[2]*256)
        #    ty = data[3] + (data[4]*256)
            Z_push = data[5] + (data[6]*256)

        #    #なぞ
        #    if data[2] > 127:
        #        tx -= 65536
        #    if data[4] > 127:
        #        ty -= 65536
            if data[6] > 127:
                Z_push -= 65536

            if Z_push <= Z_DED_ZONE and Z_push >= -Z_DED_ZONE:
                Z_push = 0

            diff = abs(Z_push - old_Z_push)
            if diff > Z_DIFF_SIZE and sum(R_list) == 0:
                print("Push: ",Z_push)
        #    print("T: ", tx, ty, tz)

        if data[0] == 2:
            old_R_list = copy.deepcopy(R_list)
            # rotation packet
            #rx = data[1] + (data[2]*256)
            R_list[0] = data[1] + (data[2]*256)
            #ry = data[3] + (data[4]*256)
            R_list[1] = data[3] + (data[4]*256)
            #rz = data[5] + (data[6]*256)
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

            #反応の処理
            diff = abs(sum(R_list) - sum(old_R_list))
            if diff > DIFF_SIZE and abs(Z_push) < Z_DED_ZONE:
                print("R: ", R_list[0], R_list[1], R_list[2])

        if data[0] == 3:# and data[1] == 0:
            if data[1]== 0:
                print("push button : ", Button_number)
                Button_number = 0
            else:
                Button_number = data[1]
            # button packet - exit on the release
            #print("push button")
            #run = False

    except KeyboardInterrupt:
        print("end")
        break

    except usb.core.USBError:
        print("USB error")
    #except:
    #    print("read failed")
    

# end while
usb.util.dispose_resources(dev)

if reattach:
    dev.attach_kernel_driver(0)
