import json
print('initializing the configuration...')

class storedConfiguration():
    def __init__(self):
        self.credentials = {}
        try:
            with open('underwire/config/storedcreds.txt', 'r') as f:
                for line in f:
                    platform, creds = line.split(' ')
                    creds = json.loads(creds)
                    print(platform, creds)
        except Exception as e:
            print(e, ' file no there')
