from fbchat import Client, Message
from ciphers.fernet import FernetCrypt
from fbchat.models import *

class LocalMessage:
    def __init__(self, ciphertext, sender, recipient):
        self.sender = sender
        self.recipient = recipient
        self.ciphertext = ciphertext

# custom client for fbchat to allow us to access the event callbacks
class CustomClient(Client):

    def setMessageCallback(onReceive):
        self.onReceive = onReceive

    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        # Do something with message_object here
        print('onMessage received custom client')
        msg = LocalMessage(ciphertext=message_object.text, sender=message.author, recipient='self')
        self.onReceive(msg)

# main chat client for this
class FBChatClient:

    def __init__(self, msgReceivedCallback, cipherType, cipherPass, email, password):
        print('starting fbchat client')
        self.msgReceivedCallback = msgReceivedCallback
        self.client = CustomClient(email, password)
        # required for events
        #self.client.listen()

        if cipherType == 'fernet':
            self.cipherClient = FernetCrypt(password=cipherPass)
        else:
            self.cipherClient = None

    @property
    def loggedIn(self):
        print('checking login status')
        if self.client:
            return self.client.isLoggedIn()
        else:
            return False

    def login(self, email, password):
        print('starting fb login')
        if not self.client.isLoggedIn:
            self.client.login(email, password)

    # starts the fbchat client listener 
    def listen(self):


    def sendMessage(self, txt):
        if self.loggedIn:
            ciphertext = self.cipherClient.encrypt(txt)
            print('ciphertext: ', ciphertext)
            message_id = self.client.send(Message(text=ciphertext), thread_id=self.client.uid, thread_type=ThreadType.USER)

    def onReceive(self, msg):
        print('received a message')
        decrypted = self.cipherClient.decrypt(msg.ciphertext)
        print('decrypted: ', decrypted)
        msg.ciphertext = None
        msg.text = decrypted
        self.msgReceivedCallback(msg)
        return 'success'
