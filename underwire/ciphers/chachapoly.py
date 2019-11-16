import base64
import os
import random
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature

class ChachaPolyCrypt:
    # doing chachapoly with a derived key and simple counter mode nonce scheme
    def __init__(self, password):

        # initialize a send, recieve counter for creating a simple
        # incrementing nonce system
        self.send_counter, self.receive_counter = 0, 0

        password = password.encode('utf-8')
        salt = b'aaaa'  # seems the salt changes the outcome of the hash
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
            )
        key = kdf.derive(password)
        self.chacha = ChaCha20Poly1305(key)

    def generateNonce(self, counter=None, bytes=12):
        if not counter is None:
            random.seed(counter)
            return bytearray(random.getrandbits(8) for _ in range(bytes))
        return None


    def encrypt(self, plainText):
        if self.chacha:
            try:
                cipherText = self.chacha.encrypt(self.generateNonce(counter=self.send_counter, bytes=12),
                                           plainText.encode('utf-8'), None)
            except InvalidSignature:
                return None
            self.send_counter += 1
            return base64.b64encode(cipherText)

        return None

    def decrypt(self, cipherText):
        cipherText = base64.b64decode(cipherText)
        if self.chacha:
            try:
                plainText =  self.chacha.decrypt(self.generateNonce(counter=self.receive_counter, bytes=12),
                                       cipherText, None).decode('utf-8')
            except InvalidSignature:
                return None
            self.receive_counter += 1
            return plainText

        return None
