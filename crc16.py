def calc_crc16(command):
    crc_registor = 0xFFFF
    for data_byte in command:
        # CRCレジスタとデータバイトのXOR
        tmp = crc_registor ^ data_byte
        # シフト回数を記憶
        shift_num = 0
        # シフトが 8回になるまで繰り返す
        while(shift_num < 8):
            if(tmp&1 == 1): # 桁あふれが1なら
                tmp = tmp >> 1
                shift_num += 1
                tmp = 0xA001 ^ tmp
            else:
                tmp = tmp >> 1
                shift_num += 1
        # 計算結果をcrc_registorにセット
        crc_registor = tmp
    # 計算結果をbytes型へ変換
    crc = crc_registor.to_bytes(2, 'little')
    print(crc)
    # 結果を表示
    return crc