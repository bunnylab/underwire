import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QAction
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QStackedWidget, QHBoxLayout, QMainWindow
from PyQt5 import QtGui

from gui.chat_widget import ChatWidget
from gui.login_widget import LoginWidget
from gui.platformselect_widget import PlatformSelectWidget
from platforms.facebook import FBChatClient


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

        # set the initial widget
        self.initPlatformSelectWidget()

        self.setGeometry(600, 600, 500, 300)
        self.setWindowTitle('Underwire')
        self.show()

    def initPlatformSelectWidget(self):
        self.platformselectwidget = PlatformSelectWidget(self)
        self.setCentralWidget(self.platformselectwidget)
        self.platformselectwidget.fbButton.clicked.connect(lambda: self.initLoginWidget)
        self.platformselectwidget.echoButton.clicked.connect(lambda: self.initChatWidget(platform='echo'))

    def initLoginWidget(self, **kwargs):
        self.loginwidget = LoginWidget(self, **kwargs)
        self.setCentralWidget(self.loginwidget)
        self.loginwidget.connectButton.clicked.connect(self.initChatWidget)

    def initChatWidget(self, **kwargs):
        self.chatwidget = ChatWidget(self, **kwargs)
        self.setCentralWidget(self.chatwidget)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
