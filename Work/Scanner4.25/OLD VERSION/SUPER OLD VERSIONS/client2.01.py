import socket
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
sock = socket.socket.()
host='10.200.10.35'
sock.connect(host,9090)

ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imshow('frame',gray)
if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


sock.send('Hello, world!')

data = sock.recv(1024)
sock.close()

print data
