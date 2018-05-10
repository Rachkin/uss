import numpy as np
import matplotlib.pyplot as plt
import sys
import logging
import cv2
#import ftplib
from ftplib import FTP
from mpl_toolkits.mplot3d import Axes3D
import urllib
import os
import math
import time

#plt.axis('equal')
#fig = plt.figure(figsize=(300,300))
#ax = Axes3D(fig)

error1 = 0
h=640
w=480
l=100
error2 = 0

class Dots():
    def __init__(self):
        self.x = np.array([0.0])
        self.y = np.array([0.0])
        self.z = np.array([0.0])

dots = Dots()

posX = 0
posY = 0
posZ = 0
dirY = 0
dirX = 0

posXd = 0
posYd = 0
posZd = 0
print('Setup.')

#dots = np.array([0.0,0.0,0.0])

l_lower_red = np.array([0,70,50])
l_upper_red = np.array([10,255,255])

lower_dark = np.array([0,0,0])
upper_dark = np.array([103,103,103])

def Triangule(hsv):
    result = np.array([0.0,0.0,0.0]) #np.array([0.0,0.0,0.0]) for j in range(h-10)
        
    mask1 = cv2.inRange(hsv.copy(),l_lower_red,l_upper_red)
   # mask2 = cv2.inRange(hsv.copy(),u_lower_red,u_upper_red)
    mask=mask1.copy()
    
    for i in range(h-10):
        coped=mask.copy()
        crop = coped[ 0:h, i:i+10]
        cnts = cv2.findContours(crop.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
          #  print i
        cx=w
        cy=h
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
            
                        
        if alpha != 0 :
            distance=l/math.tan(alpha)
                #result[i]=(math.cos(beta)*l)/math.tan(alpha)
            posZd=math.cos((dirY+beta+2*math.pi)%(2*math.pi))*distance
            posXd=math.sin((dirY+beta+2*math.pi)%(2*math.pi))*distance
            posYd=0.0
                
 #           result[i]=np.array([posX+posXd,posY+posYd,posZ+posZd])
            result = np.vstack((result,[posX+posXd,posY+posYd,posZ+posZd]))
 #               dots = np.vstack((dots,[posX+posXd,posY+posYd,posZ+posZd]))
            dots.x = np.vstack((dots.x,[posX+posXd]))
            dots.y = np.vstack((dots.y,[posY+posYd]))
            dots.z = np.vstack((dots.z,[posZ+posZd]))
               # print(result)
    return result, dots
while True:
    
 #   ftp = FTP('addr')
 #   ftp.login()
    dangerLevel = 0;
    error = 404
    holeX=w/2
    holeY=h/2
 #   try:
 #       urllib.request.urlretrieve ("http://192.168.222.251/position.lock","position.lock")
 #   except urllib.error.HTTPError as e:
 #       error2 = e.code
 #       print(e.code)
 #   except urllib.error.URLError as e:
 #       print(e.args)

 #   if error2==404:
 #       urllib.request.urlretrieve ("http://192.168.222.251/position.txt","position.txt")
        
        
    try:
        urllib.request.urlopen ("http://192.168.222.252/archive/now.lock")
    except urllib.error.HTTPError as e:
        error1 = e.code
        print(e.code)
    except urllib.error.URLError as e:
        print(e.args)

 #   if True:
    if error1==404:
        if not os.path.isfile('/Library/WebServer/Documents/now.lock'):
            os.system('echo %s|sudo -S %s' % ('2002','touch /Library/WebServer/Documents/now.lock'))
        try:
            urllib.request.urlretrieve ("http://192.168.222.252/archive/now.jpg","now.jpg")
        except:
            continue
        img = cv2.imread("now.jpg",1)
        hsv = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2HSV)

        maskB = cv2.inRange(hsv.copy(),lower_dark,upper_dark)
        _,cnts,_ = cv2.findContours(maskB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            area = cv2.contourArea(c)
            M = cv2.moments(c)
            if area > 100 :
                dangerLevel = dangerLevel+1
                holeX =int( M['m10']/M['m00']);
                holeY =int( M['m01']/M['m00']);
                break
        black = img.copy()
        for c in cnts:
            area = cv2.contourArea(c)
            if area > 100:
                cv2.drawContours(black, c, -1, (0,0,255), 3)           

        time.sleep(0.1)
        cv2.imshow('Black',black)
        cv2.imwrite('Hole.jpg',black)
        print('Danager Level: '+ str(dangerLevel))
        if dangerLevel==1:
            print('  Hole on:           '+str(holeX)+':'+str(holeY));
            print('  Position:          '+str(posX)+':'+str(posZ));
            print('  Rotation:          '+str(dirY));
 #       result, dots = Triangule(hsv)
 #       ax.scatter(dots.z,dots.x,dots.y)
 #       plt.show()

 #       np.savetxt('result.txt',result)

        
        
        os.system('echo %s|sudo -S %s' % ('2002','rm /Library/WebServer/Documents/now.lock'))
