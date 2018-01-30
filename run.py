import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QStackedWidget, QHBoxLayout, QMainWindow

# shift to messaging menu should have
class ChatWindow(QWidget):

    def __init__(self):
        super(ChatWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # put some sort of scrolling text window
        # put some sort of text input field
        # put some sort of file menu



class LoggedWidget(QWidget):
    def __init__(self, parent=None):
        super(LoggedWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.label = QLabel('logged in!')
        layout.addWidget(self.label)
        self.setLayout(layout)


# widget for logging into discord with token
class LoginWidget(QWidget):

    def testFunction(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        retval = msg.exec_()

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QGridLayout()

        handleSelfLabel = QLabel('Your Handle')
        handleTargetLabel = QLabel('Target Handle')
        discordTokenLabel = QLabel('Discord Token')

        handleSelfEdit = QLineEdit()
        handleTargetEdit = QLineEdit()
        discordTokenEdit = QLineEdit()

        connectButton = QPushButton('Connect', self)
        connectButton.clicked.connect(self.testFunction)


        layout.addWidget(handleSelfLabel, 1, 0)
        layout.addWidget(handleSelfEdit, 1, 1)
        layout.addWidget(handleTargetLabel, 2, 0)
        layout.addWidget(handleTargetEdit, 2, 1)
        layout.addWidget(discordTokenLabel, 3, 0)
        layout.addWidget(discordTokenEdit, 3, 1)
        layout.addWidget(connectButton, 5, 2)


        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        loggedwidget = LoggedWidget(self)
        loginwidget = LoginWidget(self)
        self.central_widget.addWidget(loggedwidget)
        self.central_widget.addWidget(loginwidget)
        self.central_widget.setCurrentWidget(loginwidget)

        self.setGeometry(600, 600, 500, 300)
        self.setWindowTitle('Underwire')
        self.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
