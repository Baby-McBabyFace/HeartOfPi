#!/usr/bin/env python3
import sys
from server import Server

class Wlan:
    
    def __init__(self, host, port, obstacles):
        self.host = host
        self.port = port
        self.obstacles = obstacles
    
    def start(self):
        server = Server(self.host, self.port)
        # Wait for the PC to connect to the RPi.
        print("Listing for connection on {}:{}...".format(self.host, self.port))
        
        try:
            server.start()
        except Exception as e:
            print(e)
            server.close()
            sys.exit(1)
            
        print("Connection from {}:{} established!\n".format(server.address[0], server.address[1]))

        # Send over the obstacle data to the PC.
        print("Sending obstacle data to PC at {}:{}".format(server.address[0],server.address[1]))
        # payload = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
        payload = self.obstacles
        server.send_data(payload)
        
        print("Waiting to receive data...")
        payload = server.receive_data()
        print(payload)
        
        server.close()
        
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