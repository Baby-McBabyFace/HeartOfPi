#!/usr/bin/env python3
import sys
import configparser
import wlan
import time
import connSerial
import str2list

def estBluetooth():
    while(True):
        try:
            print("Checking Bluetooth connection...")
            bluetooth = connSerial.Serial(interface="/dev/rfcomm0")
            print("Bluetooth successfully connected")
            return bluetooth
        except Exception as e:
            print("Bluetooth not connected... Retrying in 5 seconds")
            time.sleep(5)

def estUSB():
    while(True):
        try:
            print("Checking USB connection...")
            usb = connSerial.Serial(interface="/dev/ttyUSB0", baud=115200)
            print("USB successfully connected")
            return usb
        except Exception as e:
            print("Bluetooth not connected... Retrying in 5 seconds")
            time.sleep(5)

def main():
    # Initial Variables
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    host = config.get("variables", "RPI_HOST")
    port = int(config.get("variables", "RPI_PORT"))
    
    bluetooth = estBluetooth()
    # usb = estUSB()
    
    obstacles = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
    
    while True:
        command = bluetooth.receive_command()   # Listening for Bluetooth Commands
        print(command)
        if(command == "START"):
            bluetooth.send_command(command="Converting obstacle string to list...")
            obstacles = str2list.convert(obstacles)
            bluetooth.send_command(command="Starting server...")
            break
        elif(command == "MOVE/F"):
            bluetooth.send_command(command="Robot is moving Forward")
            bluetooth.send_stm_command(move=1, x=10, y=0)
        elif(command == "MOVE/B"):
            bluetooth.send_command(command="Robot is Reversing")
        elif(command == "MOVE/R"):
            bluetooth.send_command(command="Robot is moving Right")
            # usb.send_command(command="CONTROL")
        elif(command == "MOVE/L"):
            bluetooth.send_command(command="Robot is moving Left")
            # usb.send_command(command="CONTROL")
        elif(command == "MOVE/BR"):
            bluetooth.send_command(command="Robot is Reversing Right")
            # usb.send_command(command="CONTROL")
        elif(command == "MOVE/BL"):
            bluetooth.send_command(command="Robot is Reversing Left")
            # usb.send_command(command="CONTROL")
        else:
            bluetooth.send_command(command="Obstacles updated")
            obstacles = command                
            
    wlan.Wlan(host=host, port=port, obstacles=obstacles).start()
    
if __name__ == '__main__':
    main()
