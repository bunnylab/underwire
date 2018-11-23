from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

# widget for logging into discord with token
class LoginWidget(QWidget):

    def __init__(self, parent=None, platform=None):
        super(LoginWidget, self).__init__(parent)
        self.platform = platform
        self.client = None
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        if self.platform == 'facebook':
            self.emailLabel = QLabel('Email')
            self.passwordLabel = QLabel('Password')

            self.emailEdit = QLineEdit()
            self.passwordEdit = QLineEdit()
            # stylesheets for fields
            self.emailEdit.setStyleSheet("color: black;")
            self.passwordEdit.setStyleSheet("color: black;")

            self.connectButton = QPushButton('Connect', self)

            layout.addWidget(self.emailLabel, 1, 0)
            layout.addWidget(self.emailEdit, 1, 1)
            layout.addWidget(self.passwordLabel, 2, 0)
            layout.addWidget(self.passwordEdit, 2, 1)
            layout.addWidget(self.connectButton, 4, 2)

            self.setLayout(layout)

        elif self.platform == 'discord':
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
