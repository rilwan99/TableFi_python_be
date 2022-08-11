class Account():
    def __init__(self):  # empty initialization
        self.id = []
        self.api_key = []
        self.api_secret = []

    def add_api(self, apikey, apisecret):
        try:
            self.api_key.append(apikey)
            self.api_secret.append(apisecret)
        except Exception as e:
            print('Error adding api keys')
        return
