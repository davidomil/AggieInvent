import threading


class DoorSerial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            pass

    def build_message(self,command,param1 = None, param2 = None,data = None):
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

        raise NotImplemented

