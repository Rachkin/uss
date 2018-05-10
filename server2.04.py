import socket
import numpy as np
import matplotlib.pyplot as plt
import sys

sock=socket.socket()
sock.bind(("",9090))
sock.listen(1)


date =np.array([])
while True:
    conn, addr = sock.accept()
    print('connected: ', addr)
    while True:
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
 
 #               print(i)
               
        plt.plot(data)
        plt.ylabel('graph')
        plt.show(0)
        
        #if not data:
        #     break
        print('data: ', data)
        
 #   conn.send(data.upper())

conn.close()
