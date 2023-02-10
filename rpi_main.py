#!/usr/bin/env python3
import sys
import configparser
import wlan
import time
import connSerial
import str2list
import mdpRobot
import translator
import take_pic
import bluetoothctl

def estBluetooth():
    while(True):
        try:
            print("Checking Bluetooth connection...")
            bluetooth = connSerial.Serial(interface="/dev/rfcomm0")
            print("Bluetooth successfully connected")
            return bluetooth
        except Exception as e:
            print("Bluetooth not connected... Enabling Discovery mode...")
            bl = bluetoothctl.Bluetoothctl()
            bl.make_discoverable()
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
        
        STMEND = "END"
        # obstacles = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
        obstacles = []
        while True:
            bluetooth.send_command(command="Listening to bluetooth commands...")
            command = bluetooth.receive_command()   # Listening for Bluetooth Commands
            command = command.split('/')
            instruction = command.pop(0)
            
            # Obstacle paths
            if(instruction == "START"):
                task = command.pop(0)
                
                # Task 01
                if(task == "EXPLORE"): # EXAMPLE: "START/EXPLORE/(R,04,03,0)/(00,08,10,90)/(01,12,06,-90)"
                    robot_pos = command.pop(0).replace("(", "").replace(")", "").split(",")
                    myRobot.delta(delta_x=int(robot_pos[1]), delta_y=int(robot_pos[2]))
                    bluetooth.send_command(command=myRobot.get_coords())
                    
                    obstacles = translator.android2clientTranslate(obs_data=command)
                    
                    wifi = wlan.Wlan(host=host, port=port, obstacles=obstacles)
                    wifi.start() #Connect to Laptop and send obstacle data
                    # after this part, we will receive data from the client
                    # assuming data is in list format and returning [['w030'], ['e090'], ['w050'], ['d000'], ['p001']]
                    obs_counter = 0
                    while True:
                        if(obs_counter == len(obstacles)):
                            break
                        
                        path = wifi.receive_data()
                        path = str2list.convert(path)
                        for movement in path:
                            move, val1, val2 = translator.client2stmTranslate(movement[0])
                            if(move == 7):
                                take_pic.main()
                                result = wifi.receive_data()
                                if(result != -1):
                                    obs_counter += 1
                                    wifi.send_data(payload="NEXT")
                                    bluetooth.send_command(command=result)
                            elif(val2 is None):
                                usb.send_stm_command_angle(move, val1)
                                myRobot.update_delta_turn(movement=move, angle=val1)
                            else:
                                usb.send_stm_command_axis(move, val1, val2)
                                myRobot.update_delta_straight(movement=move, distance=val2)
                            
                            command = usb.receive_stm_command()
                            if(command == STMEND):
                                bluetooth.send_command(command=myRobot.get_coords())
                                
                    wifi.send_data(payload=STMEND)
                    wifi.close()
                    
                # Task 02
                elif(task == "PATH"):
                    print("TASK #02")
            
            # Manual Movements
            elif(instruction == "MOVE"):
                direction = command.pop(0)
                
                bluetooth.send_command(command="Sending command to STM")
                if(direction == "F"):
                    usb.send_stm_command_axis(move=1, x=0, y=10)
                    myRobot.update_delta_straight(movement=1, distance=10)
                    
                elif(direction == "B"):
                    usb.send_stm_command_axis(move=2, x=0, y=-10)
                    myRobot.update_delta_straight(movement=2, distance=10)
                    
                elif(direction == "L"):
                    usb.send_stm_command_angle(move=3, angle=90)
                    myRobot.update_delta_turn(movement=3, angle=90)
                
                elif(direction == "R"):
                    usb.send_stm_command_angle(move=4, angle=90)
                    myRobot.update_delta_turn(movement=4, angle=90)

                elif(direction == "BL"):
                    usb.send_stm_command_angle(move=5, angle=90)
                    myRobot.update_delta_turn(movement=5, angle=90)

                elif(direction == "BR"):
                    usb.send_stm_command_angle(move=6, angle=90)
                    myRobot.update_delta_turn(movement=6, angle=90)
                    
                command = usb.receive_stm_command()
                if(command == STMEND):
                    bluetooth.send_command(command=myRobot.get_coords())

            # Stop Instruction
            elif(instruction == "STOP"):
                bluetooth.send_command(command="STOP")

            # Task A.3
            elif(instruction == "CUSTOMMOVE"): # "CUSTOMMOVE/F/90"
                direction = command.pop(0)
                
                bluetooth.send_command(command="Sending command to STM")
                
                distance = command.pop(0)
                
                if(direction == "F"):    
                    usb.send_stm_command_axis(move=1, x=0, y=int(distance))
                    myRobot.update_delta_straight(move=1, distance=int(distance))
                elif(direction == "B"):
                    usb.send_stm_command_axis(move=2, x=0, y=int(-distance))
                    myRobot.update_delta_straight(move=2, distance=int(distance))
                
                command = usb.receive_stm_command()
                if(command == STMEND):
                    bluetooth.send_command(command=myRobot.get_coords())
                    
            # Task A.4
            elif(instruction == "CUSTOMTURN"): # "CUSTOMMOVE/L/180"
                direction = command.pop(0)
                
                bluetooth.send_command(command="Sending command to STM")
                
                angle = command.pop(0)
                
                if(direction == "L"):
                    usb.send_stm_command_angle(move=3, angle=int(angle))
                    myRobot.update_delta_turn(movement=3, angle=int(angle))
                
                elif(direction == "R"):
                    usb.send_stm_command_angle(move=4, angle=int(angle))
                    myRobot.update_delta_turn(movement=4, angle=int(angle))

                elif(direction == "BL"):
                    usb.send_stm_command_angle(move=5, angle=int(angle))
                    myRobot.update_delta_turn(movement=5, angle=int(angle))

                elif(direction == "BR"):
                    usb.send_stm_command_angle(move=6, angle=int(angle))
                    myRobot.update_delta_turn(movement=6, angle=int(angle))
                
                command = usb.receive_stm_command()
                if(command == STMEND):
                    bluetooth.send_command(command=myRobot.get_coords())
                    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected...  Closing all connections")
        bluetooth.close()
        usb.close()
        wifi.close()
    
if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)