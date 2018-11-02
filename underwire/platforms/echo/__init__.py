class Message:
    def __init__(self, text, sender, recipient):
        self.sender = sender
        self.recipient = recipient
        self.text = text

class EchoChatClient:

    def __init__(self, msgReceivedCallback):
        print('starting echo chat client')
        self.loggedIn = True
        self.msgReceivedCallback = msgReceivedCallback

    def sendMessage(self, txt):
        if self.loggedIn:
            print('sending a message')
            msg = Message(text=txt, sender='echo', recipient='me')
            self.onReceive(msg)
            return 'success'
        else:
            return None

    def onReceive(self, msg):
        print('received a message')
        self.msgReceivedCallback(msg)
        return 'success'
