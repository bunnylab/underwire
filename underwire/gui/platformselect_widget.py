from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton

# TODO:
# add another menu for creating, joining a particular room before you
# select the cipher being used

# shift to messaging menu should have
class PlatformSelectWidget(QWidget):

    def __init__(self, parent=None):
        super(PlatformSelectWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        #self.fbLabel = QLabel('Facebook Chat')
        self.echoLabel = QLabel('Echo Test')
        self.gistLabel = QLabel('Gist')
        #self.twitterLabel = QLabel('Twitter DM (not supported)')
        #self.discordLabel = QLabel('Discord Chat')

        #self.fbButton = QPushButton('Connect', self)
        self.echoButton = QPushButton('Connect', self)
        self.gistButton = QPushButton('Connect', self)
        #self.twitterButton = QPushButton('Connect', self)
        #self.discordButton = QPushButton('Connect', self)

        #layout.addWidget(self.fbLabel, 1, 0)
        #layout.addWidget(self.fbButton, 1, 1)
        layout.addWidget(self.echoLabel, 1, 0)
        layout.addWidget(self.echoButton, 1, 1)
        layout.addWidget(self.gistLabel, 2, 0)
        layout.addWidget(self.gistButton, 2, 1)
        #layout.addWidget(self.twitterLabel, 3, 0)
        #layout.addWidget(self.twitterButton, 3, 1)
        #layout.addWidget(self.discordLabel, 4, 0)
        #layout.addWidget(self.discordButton, 4, 1)

        self.setLayout(layout)
