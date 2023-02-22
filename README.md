# ❤️ HeartOfPi ❤️

## About
Interface for communication between Bluetooth Serial, USB Serial, and Server.

#### Why the name
The Raspberry Pi gives life to the robot by interfacing between different devices, allowing it to move. Why not call it the brain? Cause it doesn't sound as cool as HeartOfPi

## Installation Guide
This is the steps that I took to get everything working. Note: You can use the monitor/keyboard/mouse that the lab provides but I feel it's unnecessary as everything can be done remotely so why not

1) Download the latest 32-bit (picamera does not work on 64-bit) version of Raspberry Pi OS from [Raspberry Pi Website](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-32-bit). In my case, I downloaded `2022-09-22-raspios-bullseye-armhf.img.xz`  
2) Extract the `.img.xz` file from the archive that you've downloaded to obtain the `.img` file  
3) Use an imager tool from your respective OSes to flash the `.img` file onto the SD card. In my case, I use Linux (not arch btw) so I used `dd` to image the SD card.

        sudo dd if=2022-09-22-raspios-bullseye-armhf.img of=/dev/mmcblk0 bs=4M conv=fsync status=progress
4) After imaging, the SD card will have 2 partitions (WinOS users will not see rootfs. Do use MacOS or Linux in this step)

        rootfs
        boot
5) Drag the following files into the 2 partitions

    Note: DO NOT BLINDLY RUN `first.sh` AND `second.sh`. **LOOK THROUGH BEFORE RUNNING**  
    Reference for `userconf` and `wpa_supplicant.conf` is available on Raspberry Pi's own [Documentation](https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/configuration/headless.adoc)

        rootfs/home/pi
            - first.sh                  # Script for setup. EDIT THE TEAM NUMBER AND IP ADDRESSES BEFORE RUNNING THIS SCRIPT.
            - second.sh                 # Script for setup. EDIT THE DHCP IP ADDRESSES BEFORE RUNNING THIS SCRIPT. BEWARE THAT THIS SCRIPT WILL ENABLE AP MODE FOR RASPBERRY PI AND THIS WILL DISABLE THE ONBOARD WIFI.
            - wallpaper.png             # Very important to have shrek as our team's lucky charm
        boot
            - SSH                       # Leave this as an empty file. Needed to enable SSH at first boot
            - userconf                  # Configured with user:pass as pi:raspberry.
            - wpa_supplicant.conf       # EDIT YOUR SSID AND PSK INTO THIS FILE
6) Remove the SD card from your workstation and insert it into the Raspberry Pi
7) Power up the Raspberry Pi
8) Find the IP address of the Raspberry Pi. I used `nmap` to find the IP address

        sudo nmap -sn <IP-ADDR>/<CIDR>
9) SSH into the Raspberry Pi with username `pi` and password `raspberry`

        ssh pi@<IP-ADDR>
10) After logging in, execute `first.sh` to set up all the dependencies. The script will reboot the Raspberry Pi automatically. Beware that `sudo apt update && sudo apt upgrade -y` will take a long time.

        sudo chmod +x first.sh second.sh    # You may need to execute this command to allow execution for first.sh and second.sh
        ./first.sh
11) Once the Raspberry Pi reboots, you are able to access the Raspberry Pi using [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/). Enter the IP address of Raspberry Pi and connect using the username and password mentioned above
12) Execute `second.sh`. PLEASE INSTALL ALL DEPENDENCIES BEFORE DOING THIS AS YOU WILL NEED AN ETHERNET CABLE AFTER RUNNING THIS SCRIPT TO INSTALL ANYTHING FROM THE INTERNET

        ./second.sh
13) After the Raspberry Pi reboots after the execution of `second.sh`, you should be able to see the AP and Bluetooth set up. To access VNC, you will use the static IP address set on `first.sh`

## Quality of Life
I have included functions that may/may not improve usability of the Raspberry Pi

| Service     | Port        | Function        |
| ----------- | ----------- | ----------- |
| SSH | 22 | For headless opeartions |
| VNC | 5900 | For GUI without connecting to a physical display |
| Samba | 445 | File sharing, easy to drag/drop files onto the Raspberry Pi|
| HTTP | 80 | For Checklist |
| figlet | - | ASCII art for terminal, just for the coolness factor |

Also, `first.sh` and `second.sh` scripts are a QoL on its own. If you screw up your Raspberry Pi OS and want a clean slate, you can start from scratch without manually doing the setup :)

## Functions
The main functions for each file are:

    client.py       # A Client Class that contains function to send/receive data from a Server through sockets
    connSerial.py   # A Serial Class that contains function to send/receive data via USB serial / Bluetooth Serial
    mdpRobot.py     # A Robot Class that keeps track of (x-axis, y-axis, orientation) of the robot. 
    rpi_main.py     # Main application; i.e., run from here
    str2list.py     # Function to convert a type(String) to a type(List)
    take_pic.py     # Function to capture image on the Raspberry Pi and transmit it to a server for image processing
    translator.py   # Function to translate data between Bluetooth Device, Microcontroller, and Server
    wlan.py         # Function to send/receive data via sockets (using client.py)
    myLED.py        # Control GPIO LEDs. This is a for fun feature and is NOT NEEDED

## Requirements from different devices
These are the requirements needed from the respective devices in order to use this interface:

### Bluetooth Serial:
    
    To transmit:
    ---------------
    START/EXPLORE/{POS}/{DATA}  # Module listens to this command to start Task #01
                                # POS contains (R, x-axis, y-axis, orientation)
                                # DATA contains obstacle data (obs_num, x-axis, y-axis, orientation)

    START/PATH                  # Module listens to this command to start Task #02
    MOVE/{DIR}                  # Module listens to this command to move in the direction that is in the command 
    CUSTOMMOVE/{DIR}/{DIST}     # Module listens to this command to move in STRAIGHT direction with a custom distance
    CUSTOMTURN/{DIR}/{DEG}      # Module listens to this command to ROTATE with a custom angle
    BULLSEYE                    # Module listens to this command to clear checklist A.5

    To Receive:
    ---------------
    STATUS/Ready to start       # Sends everytime it listens for Bluetooth Commands
    FINISH/EXPLORE              # Sends after Task #01
    FINISH/PATH                 # Sends after Task #02
    ROBOT/{X}/{Y}/{ORI}         # Sends the x-axis, y-axis, and orientation of the robot after each move.
    TARGET/{idx}/{result}       # Sends the Target ID with its corresponding image encoded value
    STOP                        # Stops all movement (not implemented yet)

### USB Serial:
    
    To transmit:
    ---------------
    Movement Done!                              # Module listens to this command to signify that the Microcontroller has completed a move

    To Receive:
    ---------------
    # E.G., \0x01\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x0A\0x00\ (Move forward 1 step)
    10-byte data with 0x01 or 0x02 at 1st byte  # Sends to tell Microcontroller to move forward/backwards, with x-axis and y-axis encoded

    # E.G., \0x03\0x00\0x00\0x00\0x5A\0x00\ (Turn left 90 degree)
    6-byte data with 0x03 - 0x06 at 1st byte    # Sends to tell Microcontroller to rotate, with angle encoded

### Server:
    
    To transmit:
    ---------------
    [['w030'], ['e090'], ['w050'], ['p000']]    # Module listens to this output from Server to start moving the Robot

    To Receive:
    ---------------
    [[85, 95, 90, 1], [125, 135, -90, 2]]       # Sends to the server for the server to compute the path

## Example of how it works (Long read, but important)
1) The module will start by checking whether the following connections are up  
a. Bluetooth Serial  
b. USB Serial  
c. Server (Socket)  
2) Once all connections are up, sends `STATUS/Ready to start` to Bluetooth Device and listens for a command from Bluetooth Device
3) Bluetooth Device sends `START/EXPLORE/(R,04,03,0)/(00,08,10,90)/(01,12,06,-90)` to module
4) Module will do the following to convert the data into something that the server can process:  
a. Split the command received and check the first command `START`  
b. Checks the next command `EXPLORE`  
c. Updates the current Robot Coordinates `(R,04,03,0)`  
d. Translates the remaining obstacle data from `(00,08,10,90)/(01,12,06,-90)` to `[[85, 95, 90, 1], [125, 135, -90, 2]]`  
5) Send the converted data `[[85, 95, 90, 1], [125, 135, -90, 2]]` to Server
6) Server will return `[[3, 2, 1], ['w030'], ['e090'], ['w050'], ['p000']]`
7) Module will then convert the data into something that the microcontroller can process:  
a. Split the command received and this data `[3, 2, 1]` contains the order that the robot will move (obs 3, obs 2, then obs 1 in this case)  
b. Take in the next command `[w030]` and converts it to `\0x01\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x1E\0x00\`, then sends the command to the microcontroller  
c. After microcontroller moves, it sends back `Move completed!`  
d. Update Bluetooth Device with coordinates `ROBOT/{X}/{Y}/{ORI}`  
e. Repeat steps b - d  
f. If step b contains a command with `[p000]`, will initiate photo taking `take_pic.py` and it returns the result with image encoded value  
g. Update Bluetooth Device with image encoded value `TARGET/{idx}/{result}`  
h. Repeat steps till end of command
8) Return to Step 02
