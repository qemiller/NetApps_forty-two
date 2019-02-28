#!/usr/bin/env python3
import socket
import wolframal:wpha   # pip install wolframalpha
import sys
from watson_developer_cloud import TextToSpeechV1
from cryptography.fernet import Fernet #must 'pip install cryptography' to have this library
import pyaudio #pip3 install pyaudio (cannot get working on my windows machine at the moment)
import wave
import pickle
import hashlib
import apikeys

def read_out_question(decrypted_question):
    text_to_speech = TextToSpeechV1(
        iam_apikey='A4D3ItyCewTNN7QxozHRgTv7zro8FOvWM0OmAsAUitYE',
        url='https://stream.watsonplatform.net/text-to-speech/api'
    )
    with open('question.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                decrypted_question,
                'audio/wav',
                'en-US_AllisonVoice'
            ).get_result().content)
    # example from stackoverflow user: zhangyangyu question: 17657103
    # define stream chunk
    chunk = 1024

    # open a wav format music
    f = wave.open(r"question.wav", "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()
    # end example from stackoverflow user: zhangyangyu question: 17657103

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a socket
port = str(sys.argv[2]) #define the port on which you went to connect
size = sys.argv[4]
ip_address = socket.gethostbyname(socket.gethostname())
s.bind((ip_adress , port))
print("[Checkpoint 01]Created socket at ",ip_address," on port ",port)
s.listen(1) #listening mode
print("[Checkpoint 02] Listening for client connections")

while True:
    client, address=s.accept()
    print("[Checkpoint 03] Accepted client connection from ",address," on port ",port)
    readIN= client.recv(1024)
    data = pickle.loads(readIN)
    print ("[Checkpoint 04] Received data ",data)
    checkSumQuestion = hashlib.md5(data[1])
    if checkSumQuestion != data[2]:
        client.send(b'checksum incorrect')
    f = Fernet(data[0])
    question = f.decrypt(data[1])
    print("[Checkpoint 05] Decrypt: Key: ",data[0]," | Plain text: ",question)
    print("[Checkpoint 06] Speaking Question: ",question)
   
    #wolframalpha	 
    print("[Checkpoint 07] Sending question to Wolframalpha: ",question)
    wolf = wolframallpha.Client(apikeys.wolframID)
    res = wolf.query(question)  #sent the question
    ans = next(res.results).text  #get the anwer
    print("[Checkpoint 08] Received answer from Wolframalpha: ",ans)
    encAns = f.encrypt(ans)
    print("[Checkpoint 09] Encrypt: Key: ", key," | Ciphertext: ", encAns)
    checkSumAns = hashlib.md5(encAns)
    print("[Checkpoint 10] Generated MD5 Checksum: ",checkSumAns)
    packet = (encAns, checkSumAns)
    pickPacket = pickle.dump(packet)
    print("[Checkpoint 11] Sending answer: ",packet)
    client.send(pickPacket)
    
client.close()
