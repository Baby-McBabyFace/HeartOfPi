#!/usr/bin/env python3
import sys
from server import Server

class Wlan:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = Server(self.host, self.port)
    
    def main(self, obstacles):
        # Send over the obstacle data to the PC.
        print("Sending obstacle data to PC at {}:{}".format(self.server.address[0], self.server.address[1]))
        # payload = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
        payload = obstacles
        self.server.send_data(payload)
        
        print("Sent obstacle data to Laptop")
    
    def start_server(self):
        # Wait for the PC to connect to the RPi.
        print("Listing for connection on {}:{}...".format(self.host, self.port))
        
        try:
            self.server.start()
        except Exception as e:
            print(e)
            self.server.close()
            sys.exit(1)
            return 0
            
        print("Connection from {}:{} established!\n".format(self.server.address[0], self.server.address[1]))
    
    def receive_data(self):        
        print("Waiting to receive data...")
        payload = self.server.receive_data()
        print(f"Received from Laptop: {payload}")
        return payload
        
    def send_data(self, payload):
        print(f"Sending to Laptop: {payload}")        
        self.server.send_data(payload=payload)
        
    def close(self):
        self.server.close()
        
        # # Receive commands from the PC.
        # print("Receiving robot commands from PC...")
        # try:
        #     commands = server.receive_data()
        #     print("Commands received!\n")
        #     print(commands)
        # except Exception as e:
        #     print(e)
        # finally:
        #     server.close()