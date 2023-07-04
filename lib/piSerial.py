from serial import Serial
from struct import pack as struct_pack

class SerialOutput:
    def __init__(self,
        port="/dev/ttyS0",
        baudrate=9600,
        timeout = 1,
        debug = False):
        self._serial_port = Serial(port, baudrate=baudrate, timeout=timeout)
        self._debug = debug

    def send_data(self, data):
        try:
            packed_data = struct_pack('>I', data)
            self._serial_port.write(packed_data)
            if self._debug:
                print("Data sent successfully:", packed_data.hex())  # Convert packed_data to hex string
        except Exception as e:
            if self._debug:
                print("Error sending data:", str(e))
