import serial
import struct
import time

# Configure serial communication
serial_port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

def send_data(data):
    try:
        # Pack the four bytes into a 32-bit value
        packed_data = struct.pack('>I', data)

        # Send the packed data to the Arduino
        serial_port.write(packed_data)
        print("Data sent successfully:", packed_data.hex())  # Convert packed_data to hex string
    except Exception as e:
        print("Error sending data:", str(e))
    time.sleep(0.01)

# Example usage
if __name__ == "__main__":
    send_data(0x01020304)
    send_data(0x21110905)
