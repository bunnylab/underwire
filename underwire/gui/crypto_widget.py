from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import QSize, QRect


class CryptoWidget(QWidget):

    def __init__(self, parent=None, platform=None):
        super(CryptoWidget, self).__init__(parent)
        self.initUI()

        self.etypeCombo.currentIndexChanged.connect(self.selectionChange)

    def initUI(self):
        layout = QGridLayout()

        self.etypeLabel = QLabel('Algorithm')
        self.etypeCombo = QComboBox(self)
        self.etypeCombo.setGeometry(QRect(40, 40, 491, 31))
        self.etypeCombo.setObjectName(("etypeCombo"))
        self.etypeCombo.addItem("Fernet Cipher with Pass")
        self.etypeCombo.addItem("ChaCha20Poly1305 PBKDF")
        self.etypeCombo.addItem("placeholder2")

        self.passwordLabel = QLabel('Password')
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.useCryptoButton = QPushButton('Select', self)

        layout.addWidget(self.etypeLabel, 1, 0)
        layout.addWidget(self.etypeCombo, 1, 1)
        layout.addWidget(self.passwordLabel, 2, 0)
        layout.addWidget(self.passwordEdit, 2, 1)
        layout.addWidget(self.useCryptoButton, 3, 1)

        self.setLayout(layout)

    # TODO: using labels for branching logic is kind of akward change pls
    def selectionChange(self,i):
        pbkdf_types = ['Fernet Cipher with Pass', 'ChaCha20Poly1305 PBKDF']

        print('changed to', self.etypeCombo.currentText())
        if self.etypeCombo.currentText() in pbkdf_types:
            self.passwordLabel.setVisible(True)
            self.passwordEdit.setVisible(True)
        else:
            self.passwordLabel.setVisible(False)
            self.passwordEdit.setVisible(False)
