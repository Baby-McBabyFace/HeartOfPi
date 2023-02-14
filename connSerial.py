import serial
import struct

class Serial:
    def __init__(self, interface, baud=9600):
        self.interface = interface
        self.baud = baud
        self.ser = serial.Serial(self.interface, self.baud)
        
    def send_command(self, command):
        print(f"Sending to BT: {command}")
        command = str.encode(command)
        self.ser.write(command)
        
    def receive_command(self):
        command = self.ser.readline().decode().strip()
        print(f"Received from BT: {command}")
        return command
    
    def send_stm_command_axis(self, move, x, y):
        command = struct.pack('>biib', move, x, y, 0)
        print(f"Sending to STM: {command}")
        self.ser.write(command)

    def send_stm_command_angle(self, move, angle):
        command = struct.pack('>bib', move, angle, 0)
        print(f"Sending to STM: {command}")
        self.ser.write(command)

    def send_stm_command_task02(self, move):
        command = struct.pack('>b', move)
        print(f"Sending to STM: {command}")
        self.ser.write(command)

    def receive_stm_command(self):
        command = self.ser.readline().decode().strip()
        print(f"Received from STM: {command}")
        return command
    
    def close(self):
        self.ser.close()
