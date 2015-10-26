#!/usr/bin/env python
# Two_Buttons_Callback.py
# Detecting Rising and Falling Edge on
# two pushbutton connected to +3.3 and GND
# Button One uses a callback function to eliminate blocking
# All callbacks operate on single thread so sequential if using multiple

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttonOne = 17     #Connected to 3.3 volts
buttonTwo = 27     #Connected to GND

# When we push buttonOne it connects +3.3 volts to input pin 17
# GPIO.PUD_DOWN "pulls" the pin low (ground) so it can detect 
# the "high" that the button sends when pushed
GPIO.setup(buttonOne, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# When we push buttonTwo it connects ground to input pin 27
# GPIO.PUD_UP "pulls" the pin to a high (+3.3 volts) so it can detect
# the "low" that the button sends when pushed
GPIO.setup(buttonTwo, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Create callback function for button one
def printFunction(channel):
    print("Button one pressed")

# Add callback function to GPIO.Rising event on buttonOne (add bouncetime=300)
GPIO.add_event_detect(buttonOne, GPIO.RISING, callback=printFunction) 

try:
    while True:
    
        GPIO.wait_for_edge(buttonTwo, GPIO.FALLING)
        print("Button two pressed")

        GPIO.wait_for_edge(buttonTwo, GPIO.RISING)
        print("Button two released")
except KeyboardInterrupt:
    GPIO.cleanup()
