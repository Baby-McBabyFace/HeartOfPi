#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

class myLED:
    def __init__(self, gpioPin, power):
        self.gpioPin = gpioPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioPin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpioPin, 100)
        self.power = power

    def up(self):
        # GPIO.output(self.gpioPin, GPIO.HIGH)
        self.pwm.start(self.power)
        
    def down(self):
        # GPIO.output(self.gpioPin, GPIO.LOW)
        self.pwm.stop()
        
    def blinkers():
        for i in range(3):
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(23, GPIO.LOW)
            time.sleep(0.1)
    
    def picTaken():
        for i in range(2):
            GPIO.output(24, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(24, GPIO.LOW)
            time.sleep(0.1)
            
    def close():
        GPIO.cleanup()
