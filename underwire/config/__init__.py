import json
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

    def persist_credentials(self):
        '''
        Persists the current set of credentials to a
        configuration file.
        '''
        try:
            with open(CREDENTIALS_FILE, 'w') as f:
                json.dump(self.credentials, f)
        except Exception as e:
            print(e, 'error persisting credentials to file...')
            return False
        return True


    def retrieve_credentials(self):
        '''
        Gets the credentials from storage on disk.
        '''
        credentials = {}
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                credentials = json.load(f)
        except Exception as e:
            print(e, ' file no there')
            return False

        self.credentials = credentials
        return True
