#!/usr/bin/env python3
import socket
import wolframalpha   # pip install wolframalpha
import sys
from watson_developer_cloud import TextToSpeechV1
from cryptography.fernet import Fernet #must 'pip install cryptography' to have this library
import pickle
import hashlib
import vlc
import apikeys
from time import sleep

def read_out_text(text):
    text_to_speech = TextToSpeechV1(
        iam_apikey=apikeys.iam_apikey,
        url=apikeys.url
    )
    with open('text.mp3', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text,
                'audio/mp3',
                'en-US_AllisonVoice'
            ).get_result().content)
    sound = vlc.MediaPlayer('text.mp3')
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new('text.mp3')
    player.set_media(media)
    player.play()
    sleep(.5)
    duration = player.get_length() / 1000
    sleep(duration)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket
port = str(sys.argv[2]) #define the port on which you went to connect
size = sys.argv[4]
ip_address = socket.gethostbyname(socket.gethostname())
s.bind(('', int(port)))
print("[Checkpoint 01] Created socket at ",ip_address," on port ",port)
s.listen(5) #listening mode
print("[Checkpoint 02] Listening for client connections")

while True:
    client, address=s.accept()
    print("[Checkpoint 03] Accepted client connection from ",address," on port ",port)
    readIN= client.recv(1024)
    data = pickle.loads(readIN)
    print ("[Checkpoint 04] Received data ", data)
    checkSumQuestion = hashlib.md5(data[1])
    if checkSumQuestion != data[2]:
        client.send(b'checksum incorrect')
    f = Fernet(data[0])
    forwolfram = f.decrypt(data[1])
    question = str(forwolfram)
    #question = str(f.decrypt(data[1]))
    print("[Checkpoint 05] Decrypt: Key: ",data[0]," | Plain text: ",question)
    print("[Checkpoint 06] Speaking Question: ",question)
    read_out_text(question)

    #wolframalpha	 
    print("[Checkpoint 07] Sending question to Wolframalpha: ",question)
    wolf = wolframalpha.Client(apikeys.wolframID)
    res = wolf.query(bytes(forwolfram))  #sent the question
    ans = next(res.results).text  #get the anwer
    print("[Checkpoint 08] Received answer from Wolframalpha: ",ans)
    encAns = f.encrypt(bytes(ans,'utf-8'))
    print("[Checkpoint 09] Encrypt: Key: ", data[1]," | Ciphertext: ", encAns)
    checkSumAns = hashlib.md5(encAns)
    print("[Checkpoint 10] Generated MD5 Checksum: ",checkSumAns)
    packet = (encAns, checkSumAns)
    pickPacket = pickle.dumps(packet)
    print("[Checkpoint 11] Sending answer: ",packet)
    client.send(pickPacket)

client.close()
