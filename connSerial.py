import serial

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
    
    def close(self):
        self.ser.close()