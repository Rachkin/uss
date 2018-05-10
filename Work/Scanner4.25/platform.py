#!/usr/bin/python
import pynput
from pynput import keyboard
from pynput.keyboard import Key 
import RPi.GPIO as GPIO


M1 = 4
M2 = 3

S = 17

F = 0

H = GPIO.LOW
L = GPIO.HIGH

GPIO.setmode(GPIO.BCM)
GPIO.setup(M1,GPIO.OUT)
GPIO.setup(M2,GPIO.OUT)
GPIO.setup(F,GPIO.OUT)
GPIO.setup(S,GPIO.OUT)



GPIO.output(M1,L)
GPIO.output(M2,L)
GPIO.output(F,H)

p=GPIO.PWM(17,50)
p.start(7.5)

def on_press(key1):
    try:
        print key1
        if (key1==Key.up) or (key1 == u'w'):
            GPIO.output(M1,L)
            GPIO.output(M2,H)
        elif key1==Key.down or key1 == u's':
            GPIO.output(M1,H)
            GPIO.output(M2,L)
        if key1==Key.left or key1 == u'a':
            p.ChangeDutyCycle(4)
        elif key1==Key.right or key1 == u'd':
            p.ChangeDutyCycle(6.5)
    
          
       
            
        
    except AttributeError:
        print key1

def on_release(key):
    try:
        print key
        GPIO.output(M1,L)
        GPIO.output(M2,L)

        p.ChangeDutyCycle(5)
    except AttributeError:
        print key

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
