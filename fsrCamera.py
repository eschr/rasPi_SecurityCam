#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import picamera
from datetime import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# setting up GPIO pin for input
pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)
RUNNING = True

# setting up CAMERA 
camera = picamera.PiCamera()
resolution = (1024, 768)
camera.led = False
camera.resolution = resolution
pics_taken = 0

fromAddr = 'rpiseccam370@gmail.com'
toAddr = 'rpiseccam370@gmail.com'
userName = 'rPiSecCam370'
passWord = 'CS370project'



def pressureSensed(pin):
	print "Pressure sensed, taking pic"
	takePicture()

def sendMessage(file):
	msg = MIMEMultipart()
	msg['Subject'] = datetime.now().strftime("%a, %b %d at %H:%M")
	msg.preamble = 'Someone approached your front door'
	fp = open(file, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(userName,passWord)
	server.sendmail(fromAddr, toAddr, msg.as_string())
	server.quit()
	

def takePicture():
	global pics_taken
	print "Taking picture"
	pic_file = "img.jpg"
	camera.capture(pic_file)
        sendMessage(pic_file);
	pics_taken += 1
	print "Picture taken"
		

#loop running with event callback
try:
   GPIO.add_event_detect(pin, GPIO.RISING, callback=pressureSensed)
   while RUNNING:
	   if (GPIO.input(pin) == 1):
		print "Pressure\n"
 	   time.sleep(10)

except KeyboardInterrupt:
	print "\n quitting"

finally:
	GPIO.cleanup()
	camera.close()
