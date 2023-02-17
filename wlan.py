#!/usr/bin/env python3
import sys
from client import Client

class Wlan:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = Client(self.host, self.port)
    
    def main(self, obstacles):
        # Send over the obstacle data to the PC.
        print("Sending obstacle data to PC at {}:{}".format(self.host, self.port))
        # payload = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
        payload = obstacles
        self.client.send_data(payload)
        
        print("Sent obstacle data to Laptop")
    
    def start_client(self):
        # Wait for the PC to connect to the RPi.
        print("Connecting to {}:{}...".format(self.host, self.port))
        
        try:
            self.client.connect()
        except Exception as e:
            print(e)
            self.client.close()
            sys.exit(1)
            return 0
            
        print("Connection to {}:{} established!\n".format(self.host, self.port))
    
    def receive_data(self):        
        print("Waiting to receive data...")
        payload = self.client.receive_data()
        print(f"Received from Laptop: {payload}")
        return payload
        
    def send_data(self, payload):
        print(f"Sending to Laptop: {payload}")        
        self.client.send_data(payload=payload)
        
    def close(self):
        self.client.close()