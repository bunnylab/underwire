from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit
from PyQt5 import QtGui
from platforms.echo import EchoChatClient, Message
from platforms.facebook import FBChatClient, Message
from platforms.gistcomments import GistCommentChatClient, Message

# # TODO:
# 1) clean up a bit actually looks pretty good
# 2) add a menu item for deleting your previous messages and another for deleting the room/gist

# shift to messaging menu should have
class ChatWidget(QWidget):

    def __init__(self, parent=None, platform=None, email=None, password=None, target=None, cipherType=None, cipherPass=None, credentials=None):
        super(ChatWidget, self).__init__(parent)
        self.platform = platform
        self.chatclient = None

        if platform == 'echo':
            print('setting echo chat client')
            # this is pretty clever pass in the gui callback to whichever library
            # callback we need to use for message receipt gj me
            self.chatclient = EchoChatClient(msgReceivedCallback=self.messageReceived,
                cipherType=cipherType, cipherPass=cipherPass)

        elif platform == 'gist':
            print('setting gist chat client')
            gist_id = credentials.get('gist_id', None)
            oauth_token = credentials.get('oauth_token', None)

            self.chatclient = GistCommentChatClient(msgReceivedCallback=self.messageReceived,
                cipherType=cipherType, cipherPass=cipherPass, oauth_token=oauth_token, gist_id=gist_id)

        #elif platform == 'facebook':
        #    self.setStatusTip('Logging in to facebook with email {}...'.format(email))
        #    self.chatclient = FBChatClient(msgReceivedCallback=self.messageReceived,
        #        cipherType=cipherType, cipherPass=cipherPass,
        #        email=email, password=password, target=target)

        #elif platform == 'discord':
        #    print('setting discord chat client')

        self.setStatusTip(platform)
        self.initUI()


    def initUI(self):
        layout = QGridLayout()

        self.chatHistory = QTextEdit()
        self.chatInput = QLineEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setLineWrapMode(QTextEdit.NoWrap)

        layout.addWidget(self.chatHistory, 1, 0)
        layout.addWidget(self.chatInput, 2, 0)

        self.chatInput.setStyleSheet("color: white;")
        self.chatHistory.setStyleSheet("color: white;")

        self.setLayout(layout)

    # for sending messages
    def keyPressEvent(self, event):
         if type(event) == QtGui.QKeyEvent:
             #here accept the event and do something
             print(event.key())
             # append message to history
             #self.chatHistory.insertPlainText("{}: {}\n".format('self', self.chatInput.text()))
             # send message
             self.chatclient.sendMessage(self.chatInput.text())

             self.chatHistory.moveCursor(QtGui.QTextCursor.End)
             self.chatInput.clear()
             event.accept()
         else:
             event.ignore()

    def messageReceived(self, msg):
        self.chatHistory.insertPlainText("{}: {}\n".format(msg.sender, msg.text))
