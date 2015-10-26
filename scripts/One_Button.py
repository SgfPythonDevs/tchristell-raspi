#!/usr/bin/env python
# One_Button.py
# Reading pushbutton connected to +3.3 as input

# Alias as GPIO
import RPi.GPIO as GPIO

#Set Broadcom pin numbering
GPIO.setmode(GPIO.BCM)
# Stop warning for pins changing
GPIO.setwarnings(False)

# Define Broadcom pin the push button is connected to
buttonOne = 17

# When we push the button it connects +3.3 volts to input pin 17
# GPIO.PUD_DOWN "pulls" the ping to a low position so it can detect \
# the "high" that the button sends when pushed
GPIO.setup(buttonOne, GPIO.IN, GPIO.PUD_DOWN)

try:
    while True:
        if GPIO.input(buttonOne) == True:
            print("button one pressed")
            
except KeyboardInterrupt:
    GPIO.cleanup()

