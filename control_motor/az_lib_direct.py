from crc16 import calc_crc16

class az_motor_direct():
    def __init__(self,client,unit_id,move_list=False):
        self.client = client
        self.unit_id = unit_id.to_bytes(1,"big")
        self.move_list = move_list

    def go(self,point,speed=2000,rate=1500,stop_rate=1500):
        commando = b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x01" 
        point = point.to_bytes(4,'big')
        speed = speed.to_bytes(4,'big')
        rate  = rate.to_bytes(4,'big')
        stop_rate = stop_rate.to_bytes(4,'big')
        op_current = b"\x00\x00\x03\xE8" #100%
        trigger = b"\x00\x00\x00\x01"
        commando = self.unit_id + commando + point + speed + rate + stop_rate + op_current + trigger
        crc = calc_crc16(commando)
        commando = commando + crc
        self.client.write(commando)
        result = self.client.read()

    #1000 = 100, 1=0.1%
    def go_torque(self,op_current,point=0,speed=2000,rate=1500,stop_rate=1500):
        commando = b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x12" 
        point = point.to_bytes(4,'big')
        speed = speed.to_bytes(4,'big')
        rate  = rate.to_bytes(4,'big')
        stop_rate = stop_rate.to_bytes(4,'big')
        op_current = op_current.to_bytes(4,'big')
        trigger = b"\x00\x00\x00\x01"
        commando = self.unit_id + commando + point + speed + rate + stop_rate + op_current + trigger
        crc = calc_crc16(commando)
        commando = commando + crc
        self.client.write(commando)
        result = self.client.read()

    def go_list(self,list_number,speed=6000,rate=3000,stop_rate=3000):
        if(self.move_list):
            commando = b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x01" 
            point = self.move_list[list_number]
            point = point.to_bytes(4,'big')
            speed = speed.to_bytes(4,'big')
            rate  = rate.to_bytes(4,'big')
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

    def go_torque_pos(self,point,op_current,speed=2000,rate=1500,stop_rate=1500):
        commando = b"\x10\x00\x58\x00\x10\x20\x00\x00\x00\x00\x00\x00\x00\x14" 
        point = point.to_bytes(4,'big')
        speed = speed.to_bytes(4,'big')
        rate  = rate.to_bytes(4,'big')
        stop_rate = stop_rate.to_bytes(4,'big')
        op_current = op_current.to_bytes(4,'big')
        trigger = b"\x00\x00\x00\x01"
        commando = self.unit_id + commando + point + speed + rate + stop_rate + op_current + trigger
        crc = calc_crc16(commando)
        commando = commando + crc
        self.client.write(commando)
        result = self.client.read()

    def set_position_deviation(self,rev_value):
        commando = b"\x10\x03\x02\x00\x02\x04" 
        rev_value = rev_value.to_bytes(4,'big')
        commando = self.unit_id + commando + rev_value
        crc = calc_crc16(commando)
        commando = commando + crc
        self.client.write(commando)
        result = self.client.read()
