import socket
import numpy as np
import matplotlib.pyplot as plt
import sys
import logging
#import ftplib
from ftplib import FTP

sock=socket.socket()
sock.bind(("",9090))
sock.listen(1)



while True:
    conn, addr = sock.accept()
    print('connected: ', addr)
    ftp = FTP('addr')
    ftp.login() 
    while True:
        
        messege = conn.recv(8)
        data = messege
        if messege == b'':
           conn.close()
           print('disconnected: ', addr)
           break
        if messege == b'[1]':
            print('YELLOW ALERT')
            FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
            logging.basicConfig(format=FORMAT)
            d = {'clientip': 'localhost', 'user': 'Iam'}
            logger = logging.getLogger('tcpserver')
            logger.warning('Protocol problem: %s', 'YELLOW ALERT',extra=d)
 #           logging.log('Protocol problem: %s', 'YELLOW ALERT',extra=d)
        if messege >=  b'[2]':
            print('RED ALERT!!!')
            FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
            logging.basicConfig(format=FORMAT)
            d = {'clientip': 'localhost', 'user': 'Iam'}
            logger = logging.getLogger('tcpserver')
            logger.warning('Protocol problem: %s', 'RED ALERT!!!',extra=d)
        if messege == b'[0]':
            print('All good')
    ftp.quit()
        
               
   
        
        #if not data:
        #     break
 #       print('data: ', data)
        
 #   conn.send(data.upper())

conn.close()
