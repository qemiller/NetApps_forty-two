import key  # separate file containing a key I generated with fernet
import socket
import sys
from cryptography.fernet import Fernet #must 'pip install cryptography' to have this library

# get socket setup to contact server (from echo_client_exception.py class example)
host = '192.168.1.108' # server pi's IP address. This is from example, it will need to be one of our pi's addresses
port = 50000
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
# except socket.error, (value,message):
except socket.error as message:
    if s:
        s.close()
    print ("Unable to open the socket: " + str(message))
    sys.exit(1)

# todo decrypt qr code. This will need some soft of looped state until camera has received a valid QR input



# here we take string from QR code and encrypt it
cipher_suite = Fernet(key.fernet_key)
cipher_text = cipher_suite.encrypt(b"this will be from the QR Code instead of a literal string")
# send encrypted QR text to server via socket
s.send(cipher_text);
answer = s.recv(size)
s.close()   # might not want to close this here. Only close after client is done running.
print('[Checkpoint 04] Encrypt: ', key.fernet_key, cipher_text)

print ('Answer:', answer)