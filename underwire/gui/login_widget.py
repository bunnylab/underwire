from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from platforms.gistcomments import USER_AGENT_STRING
import requests
from requests import HTTPError

# widget for logging into stuff with token
# TODO:
# add some method of initializing with the github token so we aren't hardcoding
# it in like chumps, high priority... somehow save it option too?

class LoginWidget(QWidget):

    def __init__(self, parent=None, platform=None):
        super(LoginWidget, self).__init__(parent)
        self.platform = platform
        self.client = None
        self.initUI()

    def newGistClicked(self):
        '''
        A function to generate a new empty gist and populate its id in our
        text edit field.
        '''
        print('new gist function triggers')
        oauth_token = self.oauthtokenEdit.text()
        try:
            response = requests.post(
                headers={"Authorization":"token {}".format(oauth_token),
                         "User-Agent": USER_AGENT_STRING},
                url="https://api.github.com/gists",
                json={"public": False,
                    "files": { "randomizelater.txt":{"content":"abc"} } }
                )
            response.raise_for_status()
        except HTTPError as http_err:
            self.gistIDEdit.setText('HTTP Error generating new gist')
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            self.gistIDEdit.setText('Other Error generating new gist')
            print(f'Other error occurred: {err}')

        self.gistIDEdit.setText(response.json().get('id', ''))


    def initUI(self):
        layout = QGridLayout()

        if self.platform == 'gist':
            self.gistIDLabel = QLabel('Gist ID')
            self.gistIDEdit = QLineEdit()
            self.oauthtokenLabel = QLabel('Oauth Token')
            self.oauthtokenEdit = QLineEdit()
            self.newGistButton = QPushButton("New Gist", self)
            self.connectButton = QPushButton("Connect", self)

            self.gistIDLabel.setStyleSheet("color: white;")
            self.gistIDEdit.setStyleSheet("color: white;")
            self.oauthtokenLabel.setStyleSheet("color: white;")
            self.oauthtokenEdit.setStyleSheet("color: white;")

            layout.addWidget(self.gistIDLabel, 1, 0)
            layout.addWidget(self.gistIDEdit, 1, 1)
            layout.addWidget(self.oauthtokenLabel, 2, 0)
            layout.addWidget(self.oauthtokenEdit, 2, 1)
            layout.addWidget(self.newGistButton, 4, 0)
            layout.addWidget(self.connectButton, 4, 1)

            self.newGistButton.clicked.connect(lambda: self.newGistClicked() )

        self.setLayout(layout)

        #if self.platform == 'facebook':
        #    self.emailLabel = QLabel('Email')
        #    self.passwordLabel = QLabel('Password')
        #    self.targetLabel = QLabel('Target FB-ID:')

        #    self.emailEdit = QLineEdit()
        #    self.passwordEdit = QLineEdit()
        #    self.targetEdit = QLineEdit()
            # stylesheets for fields
        #    self.emailEdit.setStyleSheet("color: black;")
        #    self.passwordEdit.setStyleSheet("color: black;")
        #    self.targetEdit.setStyleSheet("color: black;")

        #    self.connectButton = QPushButton('Connect', self)

        #    layout.addWidget(self.emailLabel, 1, 0)
        #    layout.addWidget(self.emailEdit, 1, 1)
        #    layout.addWidget(self.passwordLabel, 2, 0)
        #    layout.addWidget(self.passwordEdit, 2, 1)
        #    layout.addWidget(self.targetLabel, 3, 0)
        #    layout.addWidget(self.targetEdit, 3, 1)
        #    layout.addWidget(self.connectButton, 5, 2)

        #    self.setLayout(layout)

        #elif self.platform == 'discord':
        #    self.handleSelfLabel = QLabel('Your Handle')
        #    self.handleTargetLabel = QLabel('Target Handle')
        #    self.discordTokenLabel = QLabel('Discord Token')

        #    self.handleSelfEdit = QLineEdit()
        #    self.handleTargetEdit = QLineEdit()
        #    self.discordTokenEdit = QLineEdit()

        #    self.connectButton = QPushButton('Connect', self)

        #    layout.addWidget(self.handleSelfLabel, 1, 0)
        #    layout.addWidget(self.handleSelfEdit, 1, 1)
        #    layout.addWidget(self.handleTargetLabel, 2, 0)
        #    layout.addWidget(self.handleTargetEdit, 2, 1)
        #    layout.addWidget(self.discordTokenLabel, 3, 0)
        #    layout.addWidget(self.discordTokenEdit, 3, 1)
        #    layout.addWidget(self.connectButton, 5, 2)

        #    self.setLayout(layout)
