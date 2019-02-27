#!/usr/bin/env python3
import socket
import wolframapha   # pip install wolframalpha

from watson_developer_cloud import TextToSpeechV1
#from cryptography.fernet import Fernet #must 'pip install cryptography' to have this library
import pyaudio #pip3 install pyaudio (cannot get working on my windows machine at the moment)
import wave

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
        # read out the question we get:
        read_out_question(question)



        # process question and get answer back.
        # answer can be text and we may have client use
        # IBM Watson to convert this to audio file and play it

        client.send(b'Thank you come agin')
    client.close()