import socket
import numpy as np
import matplotlib.pyplot as plt
import sys
import logging

sock=socket.socket()
sock.bind(("",9090))
sock.listen(1)



while True:
    conn, addr = sock.accept()
    print('connected: ', addr)
    while True:
        
        messege = conn.recv(8)
        data = messege
        if messege == b'':
           conn.close()
           print('disconnected: ', addr)
           break
        if messege == b'[1]':
            print('YELLOW ALERT')
        if messege >=  b'[2]':
            print('RED ALERT!!!')
        if messege == b'[0]':
            print('All good')
        
        
               
   
        
        #if not data:
        #     break
 #       print('data: ', data)
        
 #   conn.send(data.upper())

conn.close()
