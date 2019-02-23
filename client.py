import key  # separate file containing a key I generated with fernet
from cryptography.fernet import Fernet #must 'pip install cryptography' to have this library

# here we take string from QR code and encrypt it
cipher_suite = Fernet(key.fernet_key)
cipher_text = cipher_suite.encrypt(b"this will be from the QR Code instead of a literal string")
print('[Checkpoint 04] Encrypt: ', key.fernet_key, cipher_text)
