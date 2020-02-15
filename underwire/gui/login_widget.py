from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from platforms.gistcomments import USER_AGENT_STRING
import requests
from requests import HTTPError

# widget for logging into stuff with token
# TODO:

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
            self.setStatusTip('HTTP Error generating new gist')
            print("HTTP error occurred: {}".format(http_err))
        except Exception as err:
            self.setStatusTip('Other Error generating new gist')
            print("Other error occurred: {}".format(err))

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

            layout.addWidget(self.gistIDLabel, 1, 0)
            layout.addWidget(self.gistIDEdit, 1, 1)
            layout.addWidget(self.oauthtokenLabel, 2, 0)
            layout.addWidget(self.oauthtokenEdit, 2, 1)
            layout.addWidget(self.newGistButton, 4, 0)
            layout.addWidget(self.connectButton, 4, 1)

            self.newGistButton.clicked.connect(lambda: self.newGistClicked() )

        self.setLayout(layout)
