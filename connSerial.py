import serial
import struct

class Serial:
    def __init__(self, interface, baud=9600):
        self.interface = interface
        self.baud = baud
        self.ser = serial.Serial(self.interface, self.baud)
        
    def send_command(self, command):
        command = str.encode(command)
        self.ser.write(command)
        
    def receive_command(self):
        return self.ser.readline().decode().strip()
    
    def send_stm_command_axis(self, move, x, y):
        command = struct.pack('>biib', move, x, y, 0)
        self.ser.write(command)

    def send_stm_command_angle(self, move, angle):
        command = struct.pack('>bib', move, angle, 0)
        self.ser.write(command)

    def receive_stm_command(self):
        return self.ser.readline().decode().strip()
    
    def close(self):
        self.ser.close()
