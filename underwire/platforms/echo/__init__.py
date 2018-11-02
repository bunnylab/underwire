from ciphers.fernet import FernetCrypt

class Message:
    def __init__(self, ciphertext, sender, recipient):
        self.sender = sender
        self.recipient = recipient
        self.ciphertext = ciphertext

class EchoChatClient:

    def __init__(self, msgReceivedCallback, cipherType, cipherPass):
        print('starting echo chat client')
        print(cipherType, cipherPass)
        self.loggedIn = True
        self.msgReceivedCallback = msgReceivedCallback

        if cipherType == 'fernet':
            self.cipherClient = FernetCrypt(password=cipherPass)
        else:
            self.cipherClient = None


    def sendMessage(self, txt):
        if self.loggedIn:
            print('sending a message')
            ciphertext = self.cipherClient.encrypt(txt)
            print('ciphertext: ', ciphertext)
            msg = Message(ciphertext=ciphertext, sender='echo', recipient='me')
            self.onReceive(msg)
            return 'success'
        else:
            return None

    def onReceive(self, msg):
        print('received a message')
        decrypted = self.cipherClient.decrypt(msg.ciphertext)
        print('decrypted: ', decrypted)
        msg.ciphertext = None
        msg.text = decrypted
        self.msgReceivedCallback(msg)
        return 'success'
