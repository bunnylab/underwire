import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QAction
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QStackedWidget, QHBoxLayout, QMainWindow
from PyQt5 import QtGui

from gui.chat_widget import ChatWidget
from gui.login_widget import LoginWidget
from gui.crypto_widget import CryptoWidget
from gui.platformselect_widget import PlatformSelectWidget
from platforms.facebook import FBChatClient
from config import storedConfiguration

class MainWindow(QMainWindow):

    def __init__(self, parent=None, config=storedConfiguration()):
        super(MainWindow, self).__init__(parent)
        self.platform = None
        self.credentials = None
        self.target = None
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

        # set the initial widget
        self.initPlatformSelectWidget()

        self.setGeometry(600, 600, 500, 300)
        self.setWindowTitle('Underwire')
        self.show()


    def loginButtonClicked(self, platform):
        print('you clicked the login button')
        self.platform = platform
        if platform == 'facebook':
            self.credentials = {'email':self.loginwidget.emailEdit.text(),
                'password':self.loginwidget.passwordEdit.text()}
            self.target = {'facebook_id':self.loginwidget.targetEdit.text()}
        elif platform == 'discord':
            self.credentials = {'token':self.loginwidget.discordTokenEdit.text()}
            self.target = {'discord_id':self.loginwidget.targetEdit.text()}
        self.initCryptoWidget()


    def useCryptoButtonClicked(self, crypto):
        print('you clicked the select crypto button')
        print(crypto)
        if crypto == 'Fernet Cipher with Pass':
            cipherType = 'fernet'
            cipherPass = self.cryptowidget.passwordEdit.text()
            print(cipherPass)


        if self.platform == 'facebook':
            self.initChatWidget(platform=self.platform,
                email=self.credentials['email'],
                password=self.credentials['password'],
                target=self.target['facebook_id'],
                cipherType=cipherType,
                cipherPass=cipherPass)
        elif self.platform == 'discord':
            self.initChatWidget(platform=self.platform)  # finish implementing
        else:
            self.statusBar().showMessage('Login Failed')

    def initPlatformSelectWidget(self):
        self.platformselectwidget = PlatformSelectWidget(self)
        self.setCentralWidget(self.platformselectwidget)
        self.platformselectwidget.fbButton.clicked.connect(lambda: self.initLoginWidget(platform='facebook')) # change to login widget
        self.platformselectwidget.echoButton.clicked.connect(lambda: self.initChatWidget(platform='echo'))
        self.platformselectwidget.discordButton.clicked.connect(lambda: self.initLoginWidget(platform='discord'))

    def initLoginWidget(self, **kwargs):
        self.loginwidget = LoginWidget(self, **kwargs)
        self.setCentralWidget(self.loginwidget)
        self.loginwidget.connectButton.clicked.connect(lambda: self.loginButtonClicked(platform=self.loginwidget.platform))

    def initCryptoWidget(self, **kwargs):
        self.cryptowidget = CryptoWidget(self, **kwargs)
        self.setCentralWidget(self.cryptowidget)
        self.cryptowidget.useCryptoButton.clicked.connect(lambda: self.useCryptoButtonClicked(crypto=self.cryptowidget.etypeCombo.currentText()))

    def initChatWidget(self, **kwargs):
        self.chatwidget = ChatWidget(self, **kwargs)
        self.setCentralWidget(self.chatwidget)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
