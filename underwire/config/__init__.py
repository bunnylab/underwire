import json, cryptography
from ciphers.fernet import FernetCrypt
print('initializing the configuration...')

CREDENTIALS_FILE = 'underwire/config/storedcreds.txt'

class storedConfiguration():
    def __init__(self):
        self.credentials = {}


    def update_credentials(self, credentials, platform=None):
        '''
        Replaces current set of stored credentials with a new set.
        Does not persist, just updates locally.
        '''
        if platform:
            self.credentials[platform] = credentials
        else:
            self.credentials = credentials

    def persist_credentials(self, password=None):
        '''
        Persists the current set of credentials to a configuration file.
        Optionally takes a password which will encrypt the configuration.
        Returns a tuple (success_boolean, error_string)
        '''
        if password:
            cipher = FernetCrypt(password=password)
            encrypted_credentials = cipher.encrypt(json.dumps(self.credentials))
            credentials = encrypted_credentials.decode("utf-8")
        else:
            credentials = json.dumps(self.credentials)

        try:
            with open(CREDENTIALS_FILE, 'w') as f:
                f.write(credentials)
        except Exception as e:
            print(e, 'error persisting credentials to file...')
            return (False, 'Config file write failed.')
        return (True, None)


    def retrieve_credentials(self, password=None):
        '''
        Gets the credentials from storage on disk.
        Optionally takes a password which will decrypt the configuration.
        Returns a tuple (success_boolean, error_string)
        '''
        credentials = {}
        file_contents = None
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                file_contents = f.read()
        except Exception as e:
            print(e, ' file no there')
            return (False, 'No configuration file to load')

        if password:
            try:
                cipher = FernetCrypt(password=password)
                encoded_credentials = file_contents.encode("utf-8")
                credentials = cipher.decrypt(encoded_credentials)
            except cryptography.fernet.InvalidToken:
                return (False, 'Config decryption failed. Password invalid or config file modified.')
        else:
            credentials = file_contents

        self.credentials = json.loads(credentials)
        return (True, None)
