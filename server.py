#!/usr/bin/env python3
import socket
s= socket.socket()#create a socket

port= 50000 #defin the port on which you went to connect

s.connect(('',port))#

s.listen(5) #listening mode

while True:
    client, address=s.accept()
    print ('get connection form', address)
    readIN= client.recv(1024)
    print  ('Receiced: '+ readIN )
    if readIN:
        client.send('Thank you come agin')
    client.close()