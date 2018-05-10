import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import os
import urllib2

#cam = PiCamera()
h =640
w =480
faze = 0
#cam.resolution = (h,w)
#cam.framerate = 32
#rawCapture = PiRGBArray(cam, size=(h,w))

webCam = cv2.VideoCapture(0)

time.sleep(0.1)

P = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(P,GPIO.IN)
error=True
while True:
#for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   # cam.capture(rawCapture, format="bgr")
    time.sleep(0.3)
 #img = frame.arrayloca
    _,img = webCam.read()
   # img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    error=False
    try:
        urllib2.urlopen('http://192.168.222.254/now.lock')
    except urllib2.HTTPError as e:
        error = True
        print(e)
    except urllib2.URLError as e:
        print(e)
    if True:
        if not os.path.isfile('/var/www/html/archive/now.lock'):
            os.mknod('/var/www/html/archive/now.lock')
        cv2.imwrite('/var/www/html/archive/now.jpg',img)
        os.remove('/var/www/html/archive/now.lock')
   # rawCapture.truncate(0)
   
 

#cap.release()
cv2.destroyAllWindows()
