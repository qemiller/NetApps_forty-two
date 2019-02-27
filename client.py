from __future__ import print_function
import key  # separate file containing a key I generated with fernet
import socket
import sys
from cryptography.fernet import Fernet #must 'pip install cryptography' to have this library
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def decode(im):
    #This section taken from learnopencv.com 
    #Author: Satya Mallick

    #Find barcodes and QR Codes
    decodedObjects = pyzbar.decode(im)

    #Print results
    for obj in decodedObjects:
        print('Type: ', obj.type)
        print('Data: ', obj.data,'\n')
    
    return decodedObjects

def parseInfo(im, decodedObjects):
    
    for code in decodedObjects:
        (x,y,w,h) = code.rect
        cv2.rectangle(im,(x,y), (x+w, y+h), (0,0,255), 2)
        
        codeData = code.data.decode("utf-8")
        codeType = code.type

        text = "{} ({})".format(codeData, codeType)
        cv2.putText(im, text, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        print("[INFO] Found {} code: {}".format(codeData,codeType))

    cv2.imshow("Image", im)
    cv2.waitKey(0)

# get socket setup to contact server (from echo_client_exception.py class example)
host = '172.30.87.17' # server pi's (Rocky's) IP address.
port = 50000
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
# except socket.error, (value,message):
except socket.error as message:
    if s:
        s.close()
    print("Unable toopen the socket: " + str(message))
    sys.exit(1)

# todo decrypt qr code. This will need some soft of looped state until camera has received a valid QR input
im = cv2.imread('zbar-test.jpg')

code = decode(im)

parser(im, code)


# here we take string from QR code and encrypt it
cipher_suite = Fernet(key.fernet_key)
cipher_text = cipher_suite.encrypt(b"this will be from the QR Code instead of a literal string")
# send encrypted QR text to server via socket
s.send(cipher_text)
answer = s.recv(size)
s.close()   # might not want to close this here. Only close after client is done running.
print('[Checkpoint 04] Encrypt: ', key.fernet_key, cipher_text)

print('Answer:', answer)


