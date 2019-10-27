from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

class LocalPassWidget(QWidget):

    def __init__(self, parent=None):
        super(LocalPassWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.passwordLabel = QLabel('Stored Credentials Password')
        self.passwordEdit = QLineEdit()
        self.passwordButton = QPushButton("Continue", self)

        self.passwordEdit.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.passwordLabel, 0, 0)
        layout.addWidget(self.passwordEdit, 0, 1)
        layout.addWidget(self.passwordButton, 2, 1)

        self.setLayout(layout)
