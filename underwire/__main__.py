import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QAction
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QStackedWidget, QHBoxLayout, QMainWindow
from PyQt5 import QtGui

from message import Message
from platforms.facebook import FBChatClient

# shift to messaging menu should have
class ChatWidget(QWidget):

    def __init__(self, parent=None):
        super(ChatWidget, self).__init__(parent)
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



# widget for logging into discord with token
class LoginWidget(QWidget):

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.handleSelfLabel = QLabel('Your Handle')
        self.handleTargetLabel = QLabel('Target Handle')
        self.discordTokenLabel = QLabel('Discord Token')

        self.handleSelfEdit = QLineEdit()
        self.handleTargetEdit = QLineEdit()
        self.discordTokenEdit = QLineEdit()

        self.connectButton = QPushButton('Connect', self)

        layout.addWidget(self.handleSelfLabel, 1, 0)
        layout.addWidget(self.handleSelfEdit, 1, 1)
        layout.addWidget(self.handleTargetLabel, 2, 0)
        layout.addWidget(self.handleTargetEdit, 2, 1)
        layout.addWidget(self.discordTokenLabel, 3, 0)
        layout.addWidget(self.discordTokenEdit, 3, 1)
        layout.addWidget(self.connectButton, 5, 2)

        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # exit setup thing
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(app.quit)
        # menubar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # lets it display on mac
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        # status bar
        self.statusBar().showMessage('Ready')

        self.initLoginWidget()

        self.setGeometry(600, 600, 500, 300)
        self.setWindowTitle('Underwire')
        self.show()

    def initLoginWidget(self):
        self.loginwidget = LoginWidget(self)
        self.setCentralWidget(self.loginwidget)
        self.loginwidget.connectButton.clicked.connect(self.initChatWidget)

    def initChatWidget(self):
        self.chatwidget = ChatWidget(self)
        self.setCentralWidget(self.chatwidget)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
