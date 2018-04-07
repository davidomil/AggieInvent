import threading


class DoorSerial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            pass


    def bytes_to_int(self,bytes):
        result = 0
        for b in bytes:
            result = result * 256 + int(b)
        return result


    def int_to_bytes(self, value, length):
        result = []
        for i in range(0, length):
            result.append(value >> (i * 8) & 0xff)
        # result.reverse()
        return result


    def build_message(self, command, param1=None, param2=None, data=None):
        """
        Builds message to send over RS232
        Packet structure:
        |----------|----------------------------------|----------------|
        |  HEADER  |             DATA *               |Data Check Sum *|
        |----------|----------------------------------|----------------|
             24                Data Size                       4
        ^          ^
        |             \
        |                \
        |     Packet HEADER  \
        |------------|---------|---------|---------|-----------|------------|------------------|
        |Start Byte *| Command | Param 1 | Param 2 | Data Size | Error Code | Header Check Sum |
        |------------|---------|---------|---------|-----------|------------|------------------|
              1           4          4        4          4            4              4

        * If data size is zero, then data and data check sum is not used
        * Start byte: 0x7E

        :param command: Command to send
        :param param1: Command 1st param
        :param param2:  Command 2nd param
        :param data: Data
        :return:
        """
        msg = [b'\x7E']
        byt = bytearray(str.encode(command))
        if len(byt) < 4:
            byt.extend(b'\x00' * (4 - len(byt)))
        msg.extend([self.int_to_bytes(i,1) for i in byt[:4]])

        if param1 is None:
            param1 = ''
        one = bytearray(str.encode(param1))
        if len(one) < 4:
            one.extend(b'\x00' * (4 - len(one)))
        msg.extend([self.int_to_bytes(i,1) for i in one[:4]])

        if param2 is None:
            param2 = ''
        two = bytearray(str.encode(param2))
        if len(two) < 4:
            two.extend(b'\x00' * (4 - len(two)))
        msg.extend([self.int_to_bytes(i,1) for i in two[:4]])

        if data is None:
            data = ''
        dat = bytearray(str.encode(data))
        dat_len = self.int_to_bytes(len(dat), 4)
        msg.extend([self.int_to_bytes(i,1) for i in dat_len])

        msg.extend([self.int_to_bytes(i,1) for i in b'\x00' * 4])

        sum = 0
        for sum_el in msg:
            sum += self.bytes_to_int(sum_el)
        fin = self.int_to_bytes(sum, 4)
        msg.extend([self.int_to_bytes(i,1) for i in fin])

        return msg



