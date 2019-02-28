from __future__ import print_function
import key  # separate file containing a key I generated with fernet
import socket
import sys
from cryptography.fernet import Fernet #must 'pip install cryptography' to have this library
import pyzbar.pyzbar as pyzbar
import cv2
from picamera import PiCamera
from time import sleep
import hashlib
import pickle
import os
from watson_developer_cloud import TextToSpeechV1
import apikeys

def read_out_text(text):
    text_to_speech = TextToSpeechV1(
        iam_apikey=apikeys.iam_apikey,
        url=apikeys.url
    )
    with open('text.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text,
                'audio/wav',
                'en-US_AllisonVoice'
            ).get_result().content)
    os.system("start text.wav")  # only way i can get it to play the audio -caleb

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

# get socket setup to contact server (from echo_client_exception.py class example)
host = str(sys.argv[2]) #server pi's (Rocky's) IP address.
print(host)
port = int(sys.argv[4]) #server port
size = sys.argv[6] #server size

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("[Checkpoint 01] Connecting to ", host, "on port ", port)
# except socket.error, (value,message):
except socket.error as message:
    if s:
        s.close()
    print("Unable to open the socket: " + str(message))
    sys.exit(1)

# todo decrypt qr code. This will need some soft of looped state until camera has received a valid QR input
print("[Checkpoint 02] Listening for QR codes from RPi Camera that contain questions.")

camera = PiCamera()
camera.start_preview(fullscreen=False, window=(100,100,256,192))
sleep(5)
camera.capture('/home/pi/Documents/NetApps_forty-two/qr_code.jpg')
camera.stop_preview()
camera.close()

im = cv2.imread('qr_code.jpg')
code = decode(im)
print("[Checkpoint 03] New Question: " + code[0].data.decode("utf-8"))

# here we take string from QR code and encrypt it
cipher_suite = (Fernet(key.fernet_key))
cipher_text = cipher_suite.encrypt((code[0].data))
checksum = str(hashlib.md5(cipher_text))
# send encrypted QR text to server via socket as a tuple with the (key, question, hash)
tup = (str(key.fernet_key), cipher_text, str(checksum))
pickled_tup = pickle.dumps(tup)
print('[Checkpoint 04] Encrypt: Generated Key: ', key.fernet_key," Cipher Text: ", cipher_text)
print('[Checkpoint 05] Sending data ', tup) # print out the non-pickled version? makes more sense
s.send(pickled_tup)
received_pickle = s.recv(int(size))
# de-pickle the payload
tupans = pickle.loads(received_pickle)
print('[Checkpoint 06] Receiving data: ', received_pickle) # print out received tuple, after un-pickling

# check payload fidelity
checkSum = hashlib.md5(tupans[0])
if checkSum != tupans[1]:
    print("checksum incorrect")

# decrypt answer
answer_text = cipher_suite.decrypt(tupans[0])
print('[Checkpoint 07] Decrypt: Using Key: ', key.fernet_key, 'Plain text: ', answer_text)
# read out answer
print('[Speaking Answer: ', answer_text)
read_out_text(answer_text)

s.close()   # might not want to close this here. Only close after client is done running.

