import socket
import numpy as np
import matplotlib.pyplot as plt
from turtle import *

sock=socket.socket()
sock.bind(("",9090))
sock.listen(1)


date =np.array([])
while True:
    conn, addr = sock.accept()
    print('connected: ', addr)
    while True:
        begin_fill()
        win=GrathWin()
        data = np.array([])
        messege = conn.recv(2608)
        if messege == b'':
           conn.close()
           print('disconnected: ', addr)
           break
        
        rawdata = np.frombuffer(messege,dtype=np.uint8,count=1280)
        for i in range(1280):
            if i % 4 is 0:
                data=np.append(data,[rawdata[i]])
                dot(i,rawdata[i])
 #               print(i)
               
 #       plt.plot(data)
#        plt.ylabel('graph')
#        plt.show()
        
        #if not data:
        #     break
        print('data: ', data)
        end_fill()
        done()
        
 #   conn.send(data.upper())

conn.close()
