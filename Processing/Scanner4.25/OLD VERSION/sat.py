import socket
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from pynput import keyboard
import RPi.GPIO as GPIO
from sys import getsizeof
cam = PiCamera()
h =720
w =480
#h = 320
#w = 240
cam.resolution = (h,w)
cam.framerate = 32
rawCapture = PiRGBArray(cam, size=(h,w))

l_lower_red = np.array([0,20,0])
l_upper_red = np.array([20,255,255])

u_lower_red = np.array([150,20,0])
u_upper_red = np.array([255,255,255])

lower_dark = np.array([0,0,0])
upper_dark = np.array([255,255,63])


time.sleep(0.1)




sock = socket.socket()
host='10.200.10.61'
#host='192.168.11.35'
sock.connect((host,9090))
#cv2.namedWindow('frame',cv2.CV_WINDOW_AUTOSIZE);


for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   # cam.capture(rawCapture, format="bgr")
    time.sleep(0.1)

    answer = 0
    img = frame.array
    result = np.array([0 for j in range(h)])
    hsv = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv.copy(),l_lower_red,l_upper_red)
    mask2 = cv2.inRange(hsv.copy(),u_lower_red,u_upper_red)
    mask=mask1.copy()+mask2.copy()
    
    for i in range(h):
        cy= int(w/2)
        coped=mask.copy()
        crop = coped[0:w, i:i+5]
        cnts, hierarchy = cv2.findContours(crop.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #  print i
        for c in cnts:
            M=cv2.moments(c)
            if int(M['m00']) != 0:
                cy = int(M['m01']/M['m00'])
                
               # print cy
                break
        cv2.drawContours(img,cnts,-1,(0,255,0),3)
        result[i]=cy
    maskB = cv2.inRange(hsv.copy(),lower_dark,upper_dark)
    cnts, hierarchy = cv2.findContours(maskB.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    time.sleep(0.1)
    result[result.size-1]=np.ndarray.min(result)
    result[result.size-2]=np.ndarray.min(result)
    result[result.size-3]=np.ndarray.min(result)
    result[result.size-4]=np.ndarray.min(result)
    print result

    for c in cnts:
        answer+=1
    if answer>0:
        answer=1
    if np.ndarray.max(result)-np.ndarray.min(result)>50:
        answer+=1
        
   # if cnts is not None:
      # answer+=1
    print answer
    sock.send(bytes([answer]))
    cv2.imshow('frame',img)
    cv2.imshow('mask',mask)
    cv2.imshow('maskB',maskB)
    rawCapture.truncate(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
 

#cap.release()
cv2.destroyAllWindows()
#while(True):
    




data = sock.recv(1024)
sock.close()

print data
