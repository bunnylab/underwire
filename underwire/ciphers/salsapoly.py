import base64, os, nacl
from nacl import pwhash, utils, secret

class SalsaPolyCrypt:

    # doing salsa poly1305 with a password derived key
    def __init__(self, password):
        password = password.encode('utf-8')
        kdf = pwhash.argon2i.kdf
        salt = b'aaaabbbbccccdddd'  # 16 byte salt
        ops = pwhash.argon2i.OPSLIMIT_SENSITIVE
        mem = pwhash.argon2i.MEMLIMIT_SENSITIVE

        key = kdf(secret.SecretBox.KEY_SIZE, password, salt,
                         opslimit=ops, memlimit=mem)

        # nacl secret box
        self.box = nacl.secret.SecretBox(key)

    def encrypt(self, plaintext):
        if self.box:
            nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
            ciphertext = self.box.encrypt(plaintext.encode('utf-8'), nonce)
            encoded = base64.urlsafe_b64encode(ciphertext)
            return encoded
        else:
            return None

    def decrypt(self, cipherTxt):
        if self.box:
            decoded = base64.urlsafe_b64decode(cipherTxt)
            return self.box.decrypt(decoded).decode('utf-8')
        else:
            return None
