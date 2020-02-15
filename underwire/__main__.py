import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QAction
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QStackedWidget, QHBoxLayout, QMainWindow
from PyQt5 import QtGui

from gui.chat_widget import ChatWidget
from gui.login_widget import LoginWidget
from gui.crypto_widget import CryptoWidget
from gui.platformselect_widget import PlatformSelectWidget
from gui.localpass_widget import LocalPassWidget
from platforms.gistcomments import GistCommentChatClient
from config import storedConfiguration

WINDOW_GEOMETRY = (800,800,600,400)

class MainWindow(QMainWindow):

    def __init__(self, parent=None, config=storedConfiguration()):
        super(MainWindow, self).__init__(parent)
        self.platform = None
        self.credentials = None
        self.target = None
        self.config = config
        self.configuration_password = None

        self.initUI()

    def initUI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # exit setup thing
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(app.quit)

        # invert colors action
        darkModeAct = QAction('&Dark Mode', self)
        darkModeAct.setStatusTip('Change the colors >:(')
        darkModeAct.triggered.connect(self.colorChange)

        # menubar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # lets it display on mac
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(darkModeAct)

        # status bar
        self.statusBar().showMessage('Ready')

        # set the initial widget
        self.initLocalPassWidget()

        self.setGeometry(*WINDOW_GEOMETRY)
        self.setWindowTitle('Underwire')
        self.show()

    def colorChange(self):
        print('color change thing happened')

    def localPassClicked(self):
        '''
        Action fired when the local password button is clicked.
        '''
        self.configuration_password = self.localpasswidget.passwordEdit.text()
        (success, error) = self.config.retrieve_credentials(password=self.configuration_password)
        if error:
            self.statusBar().showMessage(error)

        self.initPlatformSelectWidget()

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
            (success, error) = self.config.persist_credentials(password=self.configuration_password)
            # set our little alert bar to error message if exists
            if error:
                self.statusBar().showMessage(error)


        self.initCryptoWidget()

    def useCryptoButtonClicked(self, crypto):
        '''
        Action fired when the crypto select button is clicked.
        '''

        if crypto == "SalsaPoly1305 Password":
            cipherType = 'salsapoly'
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

        self.platformselectwidget.echoButton.clicked.connect(lambda: self.echoPlatformClicked()) # straight to crypto
        self.platformselectwidget.gistButton.clicked.connect(lambda: self.gistPlatformClicked())

    def initLoginWidget(self, **kwargs):
        self.loginwidget = LoginWidget(self, **kwargs)
        self.setCentralWidget(self.loginwidget)
        self.loginwidget.connectButton.clicked.connect(lambda: self.loginButtonClicked(platform=self.loginwidget.platform))

    def initCryptoWidget(self, **kwargs):
        self.cryptowidget = CryptoWidget(self, **kwargs)
        self.setCentralWidget(self.cryptowidget)
        # some of the arguments in these connections can probably just
        # be done inside of the called functions
        self.cryptowidget.useCryptoButton.clicked.connect(lambda: self.useCryptoButtonClicked(crypto=self.cryptowidget.etypeCombo.currentText()))

    def initChatWidget(self, **kwargs):
        self.chatwidget = ChatWidget(self, **kwargs)
        self.setCentralWidget(self.chatwidget)

    def initLocalPassWidget(self, **kwargs):
        self.localpasswidget = LocalPassWidget(self, **kwargs)
        self.setCentralWidget(self.localpasswidget)
        self.localpasswidget.passwordButton.clicked.connect(lambda: self.localPassClicked())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
