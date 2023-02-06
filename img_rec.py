import sys
sys.path.append('/usr/lib/python3/dist-packages')

from picamera import PiCamera
from sendtopc import *

camera = PiCamera()
print("Taking photo...")
# camera.capture('/home/pi/images/image.jpg')
camera.capture('images/image.jpg')

print("photo taken")
sendImgToPC()