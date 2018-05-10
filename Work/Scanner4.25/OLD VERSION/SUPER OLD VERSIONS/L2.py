'''
Импорт Библиотек:
- OpenCV
- NumPy
- Logging
'''
:
	import cv2
	import numpy as np
	import logging
	
'''
Опрелеление переменных:
#OpenCV:
camera - переменная камеры
speed - переменная скорости записи
t - переменная времени
i - переменная номера кадра
img - переменная кадра
perimeter - переменная периметра отверстия
'''
:
	i = 0 
	camera = cv2.VideoCapture(0)
	speed = 0
	t = 100
	lower_B = np.array([0,0,0])
	upper_B = np.array([255,255,60])
	perimeter = 500
	
'''
Работаем с библиотекой OpenCV
'''
:
	def get_imageB(i):

    #img = cv2.imread('1.jpg')
    #img = cv2.imread('1.jpg')
    #img = cv2.imread('1.jpg')
    r,img = camera.read()
    r,img = camera.read()
    r,img = camera.read()

    img = cv2.blur(img,(5,5))
    
    drim = img.copy()
    #cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_B,upper_B)
    ret,thresh = cv2.threshold(mask,127,255,0)
    contours, h = cv2.findContours(thresh.copy(),1,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours

    if len(cnt) > 0:
'''
Работаем с библиотекой Logging
'''
		logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'holes.log')
