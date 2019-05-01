from crc16 import calc_crc16
import time

class blv_motor():
    def __init__(self,client,unit_id):
        self.client = client #シリアル通信用
        self.unit_id = unit_id.to_bytes(1,"big")

    #速度を設定する関数
    def set_speed(self,speed):
        commando = b"\x10\x04\x80\x00\x02\x04"
        speed = speed.to_bytes(4,'big')
        commando = self.unit_id + commando + speed
        crc = calc_crc16(commando)
        commando = commando + crc
        self.client.write(commando)
        time.sleep(0.01)
        #result = self.client.read()

    #回転開始関数(回転速度No.0)
    def go(self,fw,rev,stop=1): #fw : 正回転方向のフラグ , rev : 反対回転方向のフラグ
        commando = b"\x10\x00\x7C\x00\x02\x04\x00\x00\x00"
        data = 0
        stop = stop << 5
        rev = rev << 4
        fw  = fw  << 3
        data = data | stop
        data = data | rev
        data = data | fw
        data = data.to_bytes(1,"big")
        commando = self.unit_id + commando + data
        crc = calc_crc16(commando)
        commando = commando + crc
        self.client.write(commando)
        time.sleep(0.01)
        #result = self.client.read()

    #加減速時間の設定 1=0.1s
    def set_acc_dec_time(self,time):
        commando = b"\x10\x06\x00\x00\x02\x04"
        time = time.to_bytes(4,"big")
        commando = self.unit_id + commando + time
        crc = calc_crc16(commando)
        commando = commando + crc
        self.client.write(commando)
        result = self.client.read()

    #上記の２つをいっきに行う
    def set_speed_and_go(self,speed,fw,rev):
        self.set_speed(speed)
        self.go(fw,rev)
