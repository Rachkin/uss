import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import os

cam = PiCamera()
h =640
w =480

cam.resolution = (h,w)
cam.framerate = 32
rawCapture = PiRGBArray(cam, size=(h,w))

time.sleep(0.1)

P = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(P,GPIO.IN)

for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   # cam.capture(rawCapture, format="bgr")
    time.sleep(0.01)
    img = frame.array
    hsv = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2HSV)
    if not os.path.isfile('/var/www/html/archive/now.lock'):
        os.mknod('/var/www/html/archive/now.lock')
    cv2.imwrite('/var/www/html/archive/now.jpg',hsv)
    os.remove('/var/www/html/archive/now.lock')
    rawCapture.truncate(0)
   
 

#cap.release()
cv2.destroyAllWindows()
