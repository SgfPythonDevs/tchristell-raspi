#!/user/bin/env python

# Gmail.py
# Checks for new mail using IMAPclient and gmail account
# Uses callback to react to push button to send text message

from imapclient import IMAPClient
import time
import RPi.GPIO as GPIO

# Flag to enable debugging statements
DEBUG = True

# Used for IMAP mail retrieval
HOSTNAME = 'imap.gmail.com'
USERNAME = 'email_address@gmail.com'
PASSWORD = 'password'
MAILBOX = 'Inbox'

#Loop timer for mail check
MAIL_CHECK_FREQUENCY = 60


# SMTPLIB uses this info for sending text
global EMAIL_USER
EMAIL_USER = "tlcruns"
global EMAIL_PASSWORD
EMAIL_PASSWORD = "password"
global FROM_EMAIL_ADDRESS
FROM_EMAIL_ADDRESS = "email_address@gmail.com"
global EMAIL_TO_ADDRESS
EMAIL_TO_ADDRESS = "todd@christell.com"
global CELL_TO_ADDRESS
CELL_TO_ADDRESS = "4175551212@vtext.com"

# Flag to set number of emails
FIRST_TIME = True

# Only define one button to trigger text message
buttonOne =  17      #Connected to 3.3 volts

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Only using GREEN_LED to make things simple.  RED left in for
# example
GREEN_LED = 4
RED_LED = 23

# set both LED pins to output
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

# When we push buttonOne it connects +3.3 volts to input pin 17
# GPIO.PUD_DOWN "pulls" the pin low (ground) so it can detect 
# the "high" that the button sends when pushed
GPIO.setup(buttonOne, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Create callback function for button one
def text_Function(Channel):
    send_email("Test", " Button One Pressed", CELL_TO_ADDRESS)

# Add callback function to GPIO.Rising event on buttonOne (add bouncetime=300)
GPIO.add_event_detect(buttonOne, GPIO.RISING, callback=text_Function, bouncetime=300)


  

# ----------------------------------------------------------------------------
# send_email()
# this uses the smtplib library to generate emails, usig vtext to send text
# messages for this demo
# ----------------------------------------------------------------------------
def send_email(sub, text, to):

    import smtplib

    user = EMAIL_USER  
    pwd = EMAIL_PASSWORD
    FROM = FROM_EMAIL_ADDRESS
    TO = [to]
    SUBJECT = sub
    TEXT = text

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print "successfully sent the mail to: {}".format(to)
    except:
        print("Can't send emailto: {}".format(to))

# ----------------------------------------------------------------------------
# loop()
# loop logs into gmail account usint IMAPClient and checks for the number of
# unread email messages.  If the count is greater than last time it lights the
# LED on pin 17 for 60 seconds, which is the loop timer
# ----------------------------------------------------------------------------
 
def loop():
    global FIRST_TIME
    global NEWMAIL_OFFSET
    
    server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
    server.login(USERNAME, PASSWORD)

    if DEBUG:
        print('Loggin in as ' + USERNAME)
        select_info = server.select_folder(MAILBOX)
        print('%d messages in INBOX' % select_info['EXISTS'])

    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])

    if FIRST_TIME:
        FIRST_TIME = False
        NEWMAIL_OFFSET = newmails
        print('first time and newmail_offset is ', NEWMAIL_OFFSET)

    if newmails > NEWMAIL_OFFSET:
        print('newmails is ', newmails, ' and newmailoffset is ', NEWMAIL_OFFSET)
        NEWMAIL_OFFSET = newmails
        GPIO.output(GREEN_LED, True)
        GPIO.output(RED_LED, False)
        if DEBUG:
            print "You have", newmails, "New emails"
    else:
        print('in else and newmail_offset is ', NEWMAIL_OFFSET)
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, True)
        

    server.logout()
    time.sleep(MAIL_CHECK_FREQUENCY)


if __name__ == '__main__':
    try:
        print 'Press Ctrl-C to quit.'
        while True:
            loop()
    finally:
        GPIO.cleanup()
                       
                   
