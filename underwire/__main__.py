import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QAction
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QStackedWidget, QHBoxLayout, QMainWindow
from PyQt5 import QtGui

from gui.chat_widget import ChatWidget
from gui.login_widget import LoginWidget
from gui.crypto_widget import CryptoWidget
from gui.platformselect_widget import PlatformSelectWidget
from platforms.gistcomments import GistCommentChatClient
from config import storedConfiguration

class MainWindow(QMainWindow):

    def __init__(self, parent=None, config=storedConfiguration()):
        super(MainWindow, self).__init__(parent)
        self.platform = None
        self.credentials = None
        self.target = None
        self.config = config

        # retrieve any stored credentials
        self.config.retrieve_credentials()

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

    def echoPlatformClicked(self):
        '''
        Action fired when the echo platform select button is clicked.
        '''
        self.platform = 'echo'
        self.initCryptoWidget(platform='echo')

    def gistPlatformClicked(self):
        '''
        Action fired when the gist platform select button is clicked.
        '''
        self.platform = 'gist'
        self.initLoginWidget(platform=self.platform)

        if self.config.credentials:
            self.loginwidget.gistIDEdit.setText( self.config.credentials['gist'].get('gist_id') )
            self.loginwidget.oauthtokenEdit.setText( self.config.credentials['gist'].get('oauth_token') )

    def loginButtonClicked(self, platform):
        '''
        Action fired when the login button for a platform is clicked.
        '''
        self.platform = platform
        if platform == 'gist':
            self.credentials = {'gist_id':self.loginwidget.gistIDEdit.text(),
                                'oauth_token':self.loginwidget.oauthtokenEdit.text()}

            # add our credentials to the config file
            self.config.update_credentials(self.credentials, platform=self.platform)
            self.config.persist_credentials()

        self.initCryptoWidget()

    def useCryptoButtonClicked(self, crypto):
        '''
        Action fired when the crypto select button is clicked.
        '''
        if crypto == 'Fernet Cipher with Pass':
            cipherType = 'fernet'
            cipherPass = self.cryptowidget.passwordEdit.text()

        if self.platform == 'echo':
            self.initChatWidget(platform=self.platform,
                cipherType=cipherType,
                cipherPass=cipherPass,
                credentials=self.credentials)
        elif self.platform == 'gist':
            self.initChatWidget(platform=self.platform,
                cipherType=cipherType,
                cipherPass=cipherPass,
                credentials=self.credentials)
        else:
            self.statusBar().showMessage('Login Failed')

    def initPlatformSelectWidget(self):
        self.platformselectwidget = PlatformSelectWidget(self)
        self.setCentralWidget(self.platformselectwidget)
        #self.platformselectwidget.fbButton.clicked.connect(lambda: self.initLoginWidget(platform='facebook')) # change to login widget
        #self.platformselectwidget.echoButton.clicked.connect(lambda: self.initCryptoWidget(platform='echo')) # straight to crypto
        self.platformselectwidget.echoButton.clicked.connect(lambda: self.echoPlatformClicked()) # straight to crypto
        self.platformselectwidget.gistButton.clicked.connect(lambda: self.gistPlatformClicked())
        #self.platformselectwidget.discordButton.clicked.connect(lambda: self.initLoginWidget(platform='discord'))

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
