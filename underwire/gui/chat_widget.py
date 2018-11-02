from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit
from PyQt5 import QtGui
from message import Message

# shift to messaging menu should have
class ChatWidget(QWidget):

    def __init__(self, parent=None, platform=None):
        super(ChatWidget, self).__init__(parent)
        self.platform = platform
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

    def keyPressEvent(self, event):
         if type(event) == QtGui.QKeyEvent:
             #here accept the event and do something
             print(event.key())
             Message.sendMessage(self.chatInput.text())
             self.chatHistory.insertPlainText(self.chatInput.text() + '\n')
             self.chatHistory.moveCursor(QtGui.QTextCursor.End)
             self.chatInput.clear()
             event.accept()
         else:
             event.ignore()
