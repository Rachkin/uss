from pynput import keyboard
from pynput.keyboard import Key 
import RPi.GPIO as GPIO

L1 = 2
L2 = 3

R1 = 4
R2 = 5

F = 0

H = GPIO.LOW
L = GPIO.HIGH

GPIO.setmode(GPIO.BCM)
GPIO.setup(L1,GPIO.OUT)
GPIO.setup(L2,GPIO.OUT)
GPIO.setup(R1,GPIO.OUT)
GPIO.setup(R2,GPIO.OUT)
GPIO.setup(F,GPIO.OUT)

GPIO.output(L1,L)
GPIO.output(L2,L)
GPIO.output(R1,L)
GPIO.output(R2,L)
GPIO.output(F,H)

def on_press(key1):
    try:
        print key1
        if (key1==Key.up) or (key1 == u'w'):
            GPIO.output(L1,L)
            GPIO.output(L2,H)
            GPIO.output(R1,L)
            GPIO.output(R2,H)
        elif key1==Key.down or key1 == u's':
            GPIO.output(L1,H)
            GPIO.output(L2,L)
            GPIO.output(R1,H)
            GPIO.output(R2,L)
        elif key1==Key.left or key1 == u'a':
            GPIO.output(L1,H)
            GPIO.output(L2,L)
            GPIO.output(R1,L)
            GPIO.output(R2,H)
        elif key1==Key.right or key1 == u'd':
            GPIO.output(L1,L)
            GPIO.output(L2,H)
            GPIO.output(R1,H)
            GPIO.output(R2,L)
       
            
        
    except AttributeError:
        print key1

def on_release(key):
    try:
        print key
        GPIO.output(L1,L)
        GPIO.output(L2,L)
        GPIO.output(R1,L)
        GPIO.output(R2,L)
    except AttributeError:
        print key

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
