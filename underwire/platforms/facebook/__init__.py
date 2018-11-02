from fbchat import Client
from fbchat.models import *

class FBChatClient:
    def __init__(self):
        print('starting fbchat client')
        self.client = Client()
        self.loggedIn = False

    def login(self, username, password):
        self.client.login(username, password)

    def sendMessage(self, msg):
        if self.loggedIn:
            print('sending a message')
            return 'success'
        else:
            return None
