from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit
from PyQt5 import QtGui
from platforms.echo import EchoChatClient, Message
from platforms.facebook import FBChatClient, Message

# shift to messaging menu should have
class ChatWidget(QWidget):

    def __init__(self, parent=None, platform=None, email=None, password=None):
        super(ChatWidget, self).__init__(parent)
        self.platform = platform
        self.chatclient = None

        if platform == 'echo':
            print('setting echo chat client')
            # this is pretty clever pass in the gui callback to whichever library
            # callback we need to use for message receipt gj me
            self.chatclient = EchoChatClient(msgReceivedCallback=self.messageReceived,
                cipherType='fernet', cipherPass='awiuerfhaiufhnglasidufgasdf')

        elif platform == 'facebook':
            self.setStatusTip('Logging in to facebook with email {}...'.format(email))
            self.chatclient = FBChatClient(msgReceivedCallback=self.messageReceived,
                cipherType='fernet', cipherPass='awiuerfhaiufhnglasidufgasdf',
                email=email, password=password)

        elif platform == 'discord':
            print('setting discord chat client')

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

        self.setLayout(layout)

    # for sending messages
    def keyPressEvent(self, event):
         if type(event) == QtGui.QKeyEvent:
             #here accept the event and do something
             print(event.key())
             # append message to history
             self.chatHistory.insertPlainText("{}: {}\n".format('self', self.chatInput.text()))
             # send message
             self.chatclient.sendMessage(self.chatInput.text())

             self.chatHistory.moveCursor(QtGui.QTextCursor.End)
             self.chatInput.clear()
             event.accept()
         else:
             event.ignore()

    def messageReceived(self, msg):
        self.chatHistory.insertPlainText("{}: {}\n".format(msg.sender, msg.text))
