#!/usr/bin/env python
# Two_Buttons.py
# Reading two pushbuttons connected to +3.3 and GND as inputs

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

try:
    while True:
        if GPIO.input(buttonOne) == True:
            print("button one pressed")
        if GPIO.input(buttonTwo) == False:
            print("button two pressed")
except KeyboardInterrupt:        
    GPIO.cleanup()
