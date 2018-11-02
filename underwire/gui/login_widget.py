from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

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
