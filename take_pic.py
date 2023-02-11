import struct
import socket
import sys
import threading
import time

from picamera import PiCamera

# --- constants ---
HOST = '192.168.16.28'   # (local or external) address IP of remote server
PORT = 5001 # (local or external) port of remote server

def sendImgToPC(filename):
    
    def sender(s):
        
        f = open(f'images/{filename}.jpg','rb')

        print('Sending...')
        
        data = f.read(4096)
        while data != bytes(''.encode()):
            s.sendall(data)
            data = f.read(4096)

        print("IMG sent")
        time.sleep(3)

    try:
        # --- create socket ---
        print('[sendtopc.py] create socket')
        s = socket.socket()         
        print('[sendtopc.py] connecting:', (HOST, PORT))
        s.connect((HOST, PORT))
        print('[sendtopc.py] connected')
        
        # --- send data ---
        # sendData = threading.Thread(target=sender, args=(s,))
        # sendData.start()

        sender(s)
        label = s.recv(1024).decode()
        print('[sendtopc.py] close socket')
        s.close()
        return label

    except Exception as e:
        print(e)
    except KeyboardInterrupt as e:
        print(e)
    except:
        print(sys.exc_info())

def main():
    camera = PiCamera()
    camera.resolution=(615,462)
    fileName = time.strftime("%Y%m%d-%H%M%S")
    print("Taking photo 1...")
    camera.capture(f'images/{fileName}.jpg')
    camera.close()

    label = sendImgToPC(filename=fileName)
    print(label)
    return label
    
if __name__ == '__main__':
    main()