from ciphers.fernet import FernetCrypt
from ciphers.chachapoly import ChachaPolyCrypt
from dateutil.parser import parse
import requests, threading, time, re
from requests import HTTPError
from datetime import datetime, timezone

USER_AGENT_STRING = "underwire v0.0: experimental encrypted messaging over whatever app"
POLLING_INTERVAL = 1
MESSAGE_BLOCK = 20

def isLastPage(link_header):
    '''
    Utility function to determine if the currently requested page
    is the final available one based on the returned link header. Returns
    boolean.
    '''
    match = re.search('<https://api.github.com/gists/.+?&page=(\d+)>; rel="next"', link_header)
    if match:
        return False
    return True

class Message:
    def __init__(self, ciphertext, sender, recipient):
        self.sender = sender
        self.recipient = recipient
        self.ciphertext = ciphertext

class GistCommentChatClient:

    def __init__(self, msgReceivedCallback=None, cipherType=None, cipherPass=None, oauth_token=None, gist_id=None):
        print('starting gist chat client')
        print(cipherType, cipherPass)
        self.msgReceivedCallback = msgReceivedCallback
        self.gist_id = gist_id
        self.oauth_token = oauth_token
        self.comment_ids = []
        if self.verifyOauth(oauth_token):
            self.loggedIn = True
            self.oauth_token = oauth_token
        # starting the listener thread

        # verify the room actually exists before we get here too
        self.listener = threading.Thread(target=self.gistListener, daemon=True)
        self.listener.start()

        if cipherType == 'fernet':
            self.cipherClient = FernetCrypt(password=cipherPass)
        elif cipherType == 'chachapoly':
            self.cipherClient = ChachaPolyCrypt(password=cipherPass)
        else:
            self.cipherClient = None

    def __del__(self):
        print('deleting the gist client class')
        self.listener.join()

    def verifyOauth(self, oauth_token):
        '''
        Check that our oauth_token actually works
        '''
        return True

    def commentParser(self, data):
        '''
        Utility function to parse all comments not already stored
        and return an array of (user, ciphertext) tuples
        '''
        comments = []
        for comment in data:
            # todo timestamp parsing
            id = comment.get('id', None)
            user = comment.get('user',{}).get('login')
            created_at = parse(comment.get('created_at', None))
            ciphertext = comment.get('body', None)

            if id not in self.comment_ids:
                comments.append((user, ciphertext))
                self.comment_ids.append(id)

        return comments

    def gistListener(self):
        '''
        Threaded function to listen for new messages.
        '''
        current_page = 0
        while 1:
            try:
                if not current_page:
                    response = requests.get(
                        headers={"Authorization":"token {}".format(self.oauth_token),
                                 "User-Agent": USER_AGENT_STRING},
                        url="https://api.github.com/gists/{}/comments?per_page={}".format(self.gist_id, MESSAGE_BLOCK)
                        )
                else:
                    response = requests.get(
                        headers={"Authorization":"token {}".format(self.oauth_token),
                                 "User-Agent": USER_AGENT_STRING},
                        url="https://api.github.com/gists/{}/comments?per_page={}&page={}".format(self.gist_id, MESSAGE_BLOCK, current_page)
                        )
                response.raise_for_status()
            except HTTPError as http_err:
                print("HTTP error occurred: {}".format(http_err))
            except Exception as err:
                print("Other error occurred: {}".format(err))

            # increment pagination if there are still more comments to read
            if ('Link' in response.headers) and not isLastPage(response.headers['Link']):
                current_page += 1

            possible_messages = self.commentParser(response.json())
            for user, ciphertext in possible_messages:
                try:
                    print('ciphertext: ', ciphertext)
                    encoded = ciphertext.encode("utf-8")
                    decrypted = self.cipherClient.decrypt(encoded)
                    print('decrypted: ', decrypted)
                except Exception as e:
                    print('decryption failed')
                    print(e)
                    decrypted = 'decryption failed'

                msg = Message(None,None,None)
                msg.text = decrypted
                msg.sender = user
                self.msgReceivedCallback(msg)

            time.sleep(POLLING_INTERVAL)

    def sendMessage(self, txt):
        if self.loggedIn:
            ciphertext = self.cipherClient.encrypt(txt)
            encoded_ciphertext = ciphertext.decode("utf-8")

            try:
                response = requests.post(
                    json={"body":encoded_ciphertext},
                    headers={"Authorization":"token {}".format(self.oauth_token),
                             "User-Agent": USER_AGENT_STRING},
                    url="https://api.github.com/gists/{}/comments".format(self.gist_id)
                    )
                response.raise_for_status()
            except HTTPError as http_err:
                print("HTTP error occurred: {}".format(http_err))
            except Exception as err:
                print("Other error occurred: {}".format(err))

            return 'success'
        else:
            return None
