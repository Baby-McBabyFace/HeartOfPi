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
        
