import socket
import numpy as np
import cv2
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from pynput import keyboard
import RPi.GPIO as GPIO
from sys import getsizeof
from subprocess import call
import os
path = '/var/www/html/archive/'
fileNowTime = open(path + 'nowTime.htm','w')
fileRedTime = open(path + 'redTime.htm','w')
fileYellowTime = open(path + 'yellowTime.htm','w')
fileHoleList = open(path + 'nowHoleList.htm','w')

class Dots():
    def __init__(self):
        self.x = np.array([0.0 for j in range(h-10)])
        self.y = np.array([0.0 for j in range(h-10)])
        self.z = np.array([0.0 for j in range(h-10)])

posX = 0;
posY = 0;
posZ = 0;
dirY = 0;
dirX = 0;

startTime = time.clock()
cam = PiCamera()
h =640
w =480
#h = 320
#w = 240
cam.resolution = (h,w)
cam.framerate = 32
rawCapture = PiRGBArray(cam, size=(h,w))

l = 100

#l_lower_red = np.array([0,100,110])
#l_upper_red = np.array([40,255,255])

#u_lower_red = np.array([0,100,110])
# = np.array([0,255,255])

l_lower_red = np.array([0,70,50])
l_upper_red = np.array([10,255,255])

lower_dark = np.array([0,0,0])
upper_dark = np.array([103,103,103])


time.sleep(0.1)

P = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(P,GPIO.IN)


sock = socket.socket()
#host='10.200.10.61'
host='192.168.222.254'
#sock.connect((host,9090))
#cv2.namedWindow('frame',cv2.CV_WINDOW_AUTOSIZE);


for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   # cam.capture(rawCapture, format="bgr")
    time.sleep(0.1)

    answer = 0
    img = frame.array
    result = Dots()
    hsv = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv.copy(),l_lower_red,l_upper_red)
   # mask2 = cv2.inRange(hsv.copy(),u_lower_red,u_upper_red)
    mask=mask1.copy()
    
    for i in range(h-10):
        cy= -1
        coped=mask.copy()
        crop = coped[ 0:h, i:i+10]
        cnts, hierarchy = cv2.findContours(crop.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #  print i
        cx=0
        cy=0
        for c in cnts:
            M=cv2.moments(c)
            if int(M['m00']) != 0:
                cy = int(M['m01']/M['m00'])
                cx = int(M['m10']/M['m00'])
               # print cy
            break
     #   cv2.drawContours(img,cnts,-1,(255,0,0),3)
        cy=cy-h/2
        cx=cx-w/2
        beta=((90-24.4)/90*(math.pi/2))*(abs(cx)/(w/2))
        alpha=((90-31.1)/90*math.pi/2)*(abs(cy)/(h/2))
        
                    
        if alpha != 0:
            distance=l/math.tan(alpha)
            #result[i]=(math.cos(beta)*l)/math.tan(alpha)
            posZd=math.cos((dirY+beta+2*math.pi)%(2*math.pi))*distance
            posXd=math.sin((dirY+beta+2*math.pi)%(2*math.pi))*distance
            posYd=0.0
            
        result.x[i]=posX+posXd
        result.y[i]=posY+posYd
        result.z[i]=posZ+posZd
    cnts, hierarchy = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,cnts,-1,(255,0,0),2)
    maskB = cv2.inRange(hsv.copy(),lower_dark,upper_dark)
   # cnts, hierarchy = cv2.findContours(maskB.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    time.sleep(0.1)
    
    print result
    if not os.path.isfile('/var/www/html/resultX.lock'):
        os.mknod('/var/www/html/resultX.lock')
    np.savetxt('/var/www/html/resultX.txt',result.x)
    os.remove('/var/www/html/resultX.lock')

    if not os.path.isfile('/var/www/html/resultY.lock'):
        os.mknod('/var/www/html/resultY.lock')
    np.savetxt('/var/www/html/resultY.txt',result.y)
    os.remove('/var/www/html/resultY.lock')

    if not os.path.isfile('/var/www/html/resultZ.lock'):
        os.mknod('/var/www/html/resultZ.lock')
    np.savetxt('/var/www/html/resultZ.txt',result.z)
    os.remove('/var/www/html/resultZ.lock')
    for c in cnts:
        answer+=1
    if answer>0:
        answer=1
        
   # if cnts is not None:
      # answer+=1
    print answer
   # if GPIO.input(P) == GPIO.LOW:
    #    call("sudo shutdown -h now", shell=True)
    #sock.send(bytes([answer]))
    #cv2.imshow('frame',img)
    #cv2.imshow('mask',mask)
    #cv2.imshow('maskB',maskB)
    now = img.copy()
    #cnts, hierarchy = cv2.findContours(maskB.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(now,cnts,-1,(0,255,0),1)
    cv2.imwrite('/var/www/html/archive/now.jpg',now)
    rawCapture.truncate(0)
   
 

#cap.release()
cv2.destroyAllWindows()
#while(True):
    




data = sock.recv(1024)
sock.close()

print data
