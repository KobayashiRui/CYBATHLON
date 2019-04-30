class b3m():
    def __init__(self,client,id_list):
        self.client = client
        self.id_list = id_list

    def set_free_mode(self):
        mode = 2
        #size = 4 + len(self.id_list)
        size = 8
        command = 4
        option = 0
        address = 40
        count = len(self.id_list)
        sum_data = size + command + option + address + count + sum(self.id_list)
        data = b""
        for  i in range(len(self.id_list)):
            #speedの2の補数を求める
            sum_data += mode
            data += self.id_list[i].to_bytes(1,"little")
            data += mode.to_bytes(1,"little")
        size = size.to_bytes(1,"little")
        command = command.to_bytes(1,"little")
        option = option.to_bytes(1,"little")
        address = address.to_bytes(1,"little")
        count = count.to_bytes(1,"little")
        sum_data = (sum_data & 0xFF).to_bytes(1,"little")
        send_data = size + command + option + address + data + address + count + sum_data
        print(send_data)
        self.client.write(send_data)


    def set_speed_control_mode(self):
        mode = 4
        #size = 4 + len(self.id_list)
        size = 8
        command = 4
        option = 0
        address = 40
        count = len(self.id_list)
        sum_data = size + command + option + address + count + sum(self.id_list)
        data = b""
        for  i in range(len(self.id_list)):
            #speedの2の補数を求める
            sum_data += mode
            data += self.id_list[i].to_bytes(1,"little")
            data += mode.to_bytes(1,"little")
        size = size.to_bytes(1,"little")
        command = command.to_bytes(1,"little")
        option = option.to_bytes(1,"little")
        address = address.to_bytes(1,"little")
        count = count.to_bytes(1,"little")
        sum_data = (sum_data & 0xFF).to_bytes(1,"little")
        send_data = size + command + option + address + data + address + count + sum_data
        print(send_data)
        self.client.write(send_data)

    def set_speed_gain(self,spe)



    def send_speed_list(self,speed_list):
        if(len(self.id_list) != len(speed_list)):
            print("error")
        #size = 4 + len(self.id_list)
        size = 9
        command = 4
        option = 0
        address = 48
        count = len(self.id_list)
        sum_data = size + command + option + address + count + sum(self.id_list)
        data = b""

        for  i in range(len(self.id_list)):
            #speedの2の補数を求める
            sum_data += (speed_list[i] & 0xFF) 
            sum_data += (speed_list[i] & 0xFF00) >> 8
            data += self.id_list[i].to_bytes(1,"little")
            data += speed_list[i].to_bytes(2,"little")

        size = size.to_bytes(1,"little")
        command = command.to_bytes(1,"little")
        option = option.to_bytes(1,"little")
        address = address.to_bytes(1,"little")
        count = count.to_bytes(1,"little")
        sum_data = (sum_data & 0xFF).to_bytes(1,"little")
        send_data = size + command + option + address + data + address + count + sum_data
        print(send_data)
        self.client.write(send_data)
        

            

