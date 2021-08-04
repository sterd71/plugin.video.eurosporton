import requests

"""
  Token fetches and stores the session token
"""
class Token(object):
    def __init__(self,realm):
        self.session = requests.Session()
        self.token = self.setToken(realm)

        
    def getToken(self):
        return self.token


    def setToken(self,realm):    
        tokenResponse = self.TokenResponse(
            self.session.get(
                'https://eu3-prod-direct.eurosportplayer.com/token?realm={0}&shortlived=true'.format(realm)
            ).json()
        )
        return tokenResponse.token()


    """
       TokenResponse sends back an object containing the Eurosport session token
    """
    class TokenResponse(object):
        def __init__(self, data):
            self._data = data

        def token(self):
            return self._data.get('data.attributes.token', [])
