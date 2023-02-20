#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

class myLED:
    def __init__(self, gpioPin):
        self.gpioPin = gpioPin
        gpio.setmode(GPIO.BCM)
        GPIO.setup(self.gpioPin, GPIO.OUT)

    def up(self):
        GPIO.output(self.gpioPin, GPIO.HIGH)
        
    def down(self):
        GPIO.output(self.gpioPin, GPIO.LOW)
        
    def blink(self):
        self.up()
        time.sleep(1)
        self.down()
        
    def turning(self):
        for i in range(3):
            self.up()
            time.sleep(0.1)
            self.down
        