import socket
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
cam = PiCamera()
h =640
w =480
cam.resolution = (h,w)
cam.framerate = 32
rawCapture = PiRGBArray(cam, size=(h,w))

l_lower_red = np.array([0,80,80])
l_upper_red = np.array([20,255,255])

u_lower_red = np.array([150,80,80])
u_upper_red = np.array([255,255,255])

result = np.array([0 for j in range(h+1)])

time.sleep(0.1)



#sock = socket.socket()
#host='10.200.10.35'
#host='192.168.11.29'
#sock.connect((host,9090))
#cv2.namedWindow('frame',cv2.CV_WINDOW_AUTOSIZE);


for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   # cam.capture(rawCapture, format="bgr")
    img = frame.array
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv,l_lower_red,l_upper_red)
    mask2 = cv2.inRange(hsv,u_lower_red,u_upper_red)
    mask=mask1+mask2
    coped=mask.copy()
    for i in range(h):
        icoped = coped[i:i-1, 0:w-1]
        cnts, hierarchy = cv2.findContours(icoped,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            M=cv2.moments(c)
            if int(M['m00']) != 0:
                cy = int(M['m01']/M['m00'])
                result[i]=cy
                print cy
                break
  #  cv2.drawContours(img,contours,-1,(0,255,0),3)
    cv2.imshow('frame',img)
    cv2.imshow('mask',mask)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
#cap.release()
cv2.destroyAllWindows()
#while(True):
    


sock.send('Hello, world!')

data = sock.recv(1024)
sock.close()

print data
