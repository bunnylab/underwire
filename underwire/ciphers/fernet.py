import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class FernetCrypt:
    # doing fernet with a password derived key
    def __init__(self, password):
        password = password.encode('utf-8')
        #salt = os.urandom(16)
        salt = b'aaaa'  # seems the salt changes the outcome of the hash
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
            )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.fernet = Fernet(key)

    def encrypt(self, plaintext):
        if self.fernet:
            return self.fernet.encrypt(plaintext.encode('utf-8'))
        else:
            return 'error'

    def decrypt(self, cipherTxt):
        if self.fernet:
            return self.fernet.decrypt(cipherTxt).decode('utf-8')
        else:
            return 'error'
