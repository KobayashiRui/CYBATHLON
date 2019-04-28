from crc16 import calc_crc16

class az_motor_direct():
    def __init__(self,client,unit_id,move_list=False):
        self.client = client
        self.unit_id = unit_id.to_bytes(1,"big")
        self.move_list = move_list
    
    def go(self,point):
        commando = b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x01" 
        point = point.to_bytes(4,'big')
        speed = 2000
        speed = speed.to_bytes(4,'big')
        rate  = 1500
        rate  = rate.to_bytes(4,'big')
        stop_rate = 1500
        stop_rate = stop_rate.to_bytes(4,'big')
        op_current = b"\x00\x00\x03\xE8" #100%
        trigger = b"\x00\x00\x00\x01"
        commando = self.unit_id + commando + point + speed + rate + stop_rate + op_current + trigger
        crc = calc_crc16(commando)
        commando + crc
        self.client.write(commando)
        result = self.client.read()

    def go_list(self,list_number):
        if(self.move_list):
            commando = b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x01" 
            point = self.move_list[list_number]
            point = point.to_bytes(4,'big')
            speed = 5000
            speed = speed.to_bytes(4,'big')
            rate  = 3000
            rate  = rate.to_bytes(4,'big')
            stop_rate = 3000
            stop_rate = stop_rate.to_bytes(4,'big')
            op_current = b"\x00\x00\x03\xE8" #100%
            trigger = b"\x00\x00\x00\x01"
            commando = self.unit_id + commando + point + speed + rate + stop_rate + op_current + trigger
            crc = calc_crc16(commando)
            commando = commando + crc
            self.client.write(commando)
            result = self.client.read()
        else:
            print("Error")