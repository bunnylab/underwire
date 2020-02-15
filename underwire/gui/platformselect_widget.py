from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton

# TODO:
# add another menu for creating, joining a particular room before you
# select the cipher being used

class PlatformSelectWidget(QWidget):

    def __init__(self, parent=None):

        super(PlatformSelectWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        layout = QGridLayout()

        self.echoLabel = QLabel('Echo Test')
        self.gistLabel = QLabel('Gist')

        self.echoButton = QPushButton('Connect', self)
        self.gistButton = QPushButton('Connect', self)

        layout.addWidget(self.echoLabel, 1, 0)
        layout.addWidget(self.echoButton, 1, 1)
        layout.addWidget(self.gistLabel, 2, 0)
        layout.addWidget(self.gistButton, 2, 1)

        self.setLayout(layout)
