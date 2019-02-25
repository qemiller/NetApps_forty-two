#!/usr/bin/env python3
import socket
import wolframapha   # pip install wolframapha 

s= socket.socket()#create a socket
ID="5EK7K3-23TAQGG2UJ"
port= 50000 #defin the port on which you went to connect

s.bind(('', port))

s.listen(5) #listening mode

while True:
    client, address=s.accept()
    print ('get connection form', address)
    readIN= client.recv(1024)
    print  (b'Receiced: '+ readIN )
"""
    #wolframalpha	 
    question= wolframallpha.Client(ID)
    res = question.query(readIN)  #sent the question
    ans = next(res.results).text  #get the anwer
    print (ans +" form wolfram alpa ")

"""
    if readIN:
        client.send(b'Thank you come agin')
    client.close()
