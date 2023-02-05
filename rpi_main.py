#!/usr/bin/env python3
import sys
import configparser
import wlan
import time
import connSerial
import str2list
import mdpRobot

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
            print("USB not connected... Retrying in 5 seconds")
            time.sleep(5)

def main():
    try:
        # Initial Variables
        config = configparser.ConfigParser()
        config.read("config.ini")
        
        host = config.get("variables", "RPI_HOST")
        port = int(config.get("variables", "RPI_PORT"))
        
        myRobot = mdpRobot.Robot(x=0, y=0)
        bluetooth = estBluetooth()
        usb = estUSB()
        
        obstacles = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
        
        while True:
            bluetooth.send_command(command="Listening to bluetooth commands...")
            command = bluetooth.receive_command()   # Listening for Bluetooth Commands
            if(command == "START"):
                bluetooth.send_command(command="Converting obstacle string to list...")
                obstacles = str2list.convert(obstacles)
                bluetooth.send_command(command="Starting server...")
                break
            
            elif(command == "MOVE/F"):
                bluetooth.send_command(command="Sending command to STM")
                usb.send_stm_command_axis(move=1, x=0, y=10)
                command = usb.receive_stm_command()
                if(command == "END"):
                    bluetooth.send_command(command="Robot has moved forward")
            
            elif(command == "MOVE/B"):
                bluetooth.send_command(command="Robot is Reversing")
                usb.send_stm_command_axis(move=2, x=0, y=-10)
                command = usb.receive_stm_command()
                if(command == "END"):
                    bluetooth.send_command(command="Robot has reversed")
            
            elif(command == "MOVE/L"):
                bluetooth.send_command(command="Robot is moving Left")
                usb.send_stm_command_angle(move=3, angle=90)
                command = usb.receive_stm_command()
                if(command == "END"):
                    bluetooth.send_command(command="Robot has moved left")
            
            elif(command == "MOVE/R"):
                bluetooth.send_command(command="Robot is moving Right")
                usb.send_stm_command_angle(move=4, angle=90)
                command = usb.receive_stm_command()
                if(command == "END"):
                    bluetooth.send_command(command="Robot has moved right")

            elif(command == "MOVE/BL"):
                bluetooth.send_command(command="Robot is Reversing Left")
                usb.send_stm_command_angle(move=5, angle=90)
                command = usb.receive_stm_command()
                if(command == "END"):
                    bluetooth.send_command(command="Robot has reversed left")

            elif(command == "MOVE/BR"):
                bluetooth.send_command(command="Robot is Reversing Right")
                usb.send_stm_command_angle(move=6, angle=90)
                command = usb.receive_stm_command()
                if(command == "END"):
                    bluetooth.send_command(command="Robot has reversed right")
            
            else:
                bluetooth.send_command(command="Obstacles updated")
                obstacles = command                
                
        wifi = wlan.Wlan(host=host, port=port, obstacles=obstacles)
        wifi.start() #Connect to Laptop and send obstacle data
        while True():
            payload = wifi.receive_data()
            print(payload)
            # assuming data is in list format and returning [["f030"], ["r090"], ["f050"]]
            
        wifi.close()
        
    except KeyboardInterrupt:
        print("Keyboard interrupt detected...  Closing all connections")
        bluetooth.close()
        usb.close()
        return 0
    
if __name__ == '__main__':
    while(main()):
        main()