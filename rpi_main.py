#!/usr/bin/env python3
import sys
import configparser
import wlan
import time
import connSerial
import str2list
import mdpRobot
import translator

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
        
        # obstacles = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
        obstacles = []
        while True:
            bluetooth.send_command(command="Listening to bluetooth commands...")
            command = bluetooth.receive_command()   # Listening for Bluetooth Commands
            command = command.split('/')
            instruction = command.pop(0)
            
            if(instruction == "START"):
                task = command.pop(0)
                
                if(task == "EXPLORE"):
                    robot_pos = command.pop(0).replace("(", "").replace(")", "").split(",")
                    myRobot.delta(delta_x=int(robot_pos[1]), delta_y=int(robot_pos[2]))
                    bluetooth.send_command(command=myRobot.get_coords())
                    
                    for obs_data in command:
                        obs_data = translator.a2cTranslate(obs_data)
                        obstacles.append(obs_data)
                    
                    wifi = wlan.Wlan(host=host, port=port, obstacles=obstacles)
                    wifi.start() #Connect to Laptop and send obstacle data
                    
                elif(task == "PATH"):
                    print(2)
                
                bluetooth.send_command(command="Converting obstacle string to list...")
                obstacles = str2list.convert(obstacles)
                bluetooth.send_command(command="Starting server...")
                break
            
            elif(instruction == "MOVE"):
                direction = command.pop(0)
                
                bluetooth.send_command(command="Sending command to STM")
                if(direction == "F"):
                    usb.send_stm_command_axis(move=1, x=0, y=10)
                    myRobot.delta(delta_y=1)
                        
                elif(direction == "B"):
                    usb.send_stm_command_axis(move=2, x=0, y=-10)
                    myRobot.delta(delta_y=-1)
                    
                elif(direction == "L"):
                    usb.send_stm_command_angle(move=3, angle=90)
                    myRobot.delta(delta_x=-3, delta_y=3)
                
                elif(direction == "R"):
                    usb.send_stm_command_angle(move=4, angle=90)
                    myRobot.delta(delta_x=3, delta_y=3)

                elif(direction == "BL"):
                    usb.send_stm_command_angle(move=5, angle=90)
                    myRobot.delta(delta_x=-3, delta_y=-3)

                elif(direction == "BR"):
                    usb.send_stm_command_angle(move=6, angle=90)
                    myRobot.delta(delta_x=3, delta_y=-3)
                    
                command = usb.receive_stm_command()
                if(command == "END"):
                    bluetooth.send_command(command=myRobot.get_coords())
            
            elif(instruction == "STOP"):
                bluetooth.send_command(command="STOP")
                
        # wifi = wlan.Wlan(host=host, port=port, obstacles=obstacles)
        # wifi.start() #Connect to Laptop and send obstacle data
        # while True:
        #     payload = wifi.receive_data()
        #     print(payload)
        #     # assuming data is in list format and returning [["f030"], ["r090"], ["f050"]]
            
        
    except KeyboardInterrupt:
        print("Keyboard interrupt detected...  Closing all connections")
        bluetooth.close()
        # usb.close()
        wifi.close()
        return 0
    
if __name__ == '__main__':
    while(main()):
        main()