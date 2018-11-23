from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import QSize, QRect


class CryptoWidget(QWidget):

    def __init__(self, parent=None):
        super(CryptoWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.etypeLabel = QLabel('Algorithm')

        self.etypeCombo = QComboBox(self)
        self.etypeCombo.setGeometry(QRect(40, 40, 491, 31))
        self.etypeCombo.setObjectName(("etypeCombo"))
        self.etypeCombo.addItem("Fernet Cipher")

        self.useCryptoButton = QPushButton('Select', self)

        layout.addWidget(self.etypeLabel, 1, 0)
        layout.addWidget(self.etypeCombo, 1, 1)
        layout.addWidget(self.useCryptoButton, 2, 1)

        self.setLayout(layout)
