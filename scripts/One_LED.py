#!/usr/bin/env python

# One_LED.py
# Sets GPIO pins and illustrates driving an LED that is drived directly by GPIO
# pin 4 through a 220 ohm resistor and connected to GND

# Alias as GPIO
import RPi.GPIO as GPIO

# Used for sleep command
import time

#Set Broadcom pin numbering
GPIO.setmode(GPIO.BCM)
#Stop warnings for pins changing
GPIO.setwarnings(False)

# Define the broadcom pin the LED is connected to
ledPin = 4

# Set pin to output pin
GPIO.setup(ledPin, GPIO.OUT)

try:
    while True:
        # Turn on LED
        GPIO.output(ledPin, 1)
        # Sleep 1 second
        time.sleep(1)
        # Turn off LED
        GPIO.output(ledPin, 0)
        time.sleep(1)
except KeyboardInterrupt:
    # Reset all pins to factory state
    GPIO.cleanup()
