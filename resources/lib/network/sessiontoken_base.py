import requests

"""
  Login will login to Eurosport and get the 'st' session token
"""
class SessionToken(object):
    def __init__(self,username,password,realm,token,arkoseSiteKey,arkoseToken):
        self.session = requests.Session()
        self.session.headers = {
            'cookie': 'st={}'.format(token),
            'X-disco-arkose-sitekey': '{}'.format(arkoseSiteKey),
            'X-disco-arkose-token': '{}'.format(arkoseToken),  
            'X-disco-client': 'WEB:UNKNOWN:esplayer:prod',
            'X-disco-params': 'realm={},,'.format(realm)  
        }
        self.sessionToken = self.setSessionToken(username,password,arkoseSiteKey,arkoseToken)

        
    def getSessionToken(self):
        return self.sessionToken


    def setSessionToken(self,username,password,arkoseSiteKey,arkoseToken):
        payload = {'credentials': {'arkoseSiteKey': '{}'.format(arkoseSiteKey),
                                   'arkoseToken': '{}'.format(arkoseToken),
                                   'password': '{}'.format(password),
                                   'username': '{}'.format(username)}}
        sessionTokenResponse = self.sessionTokenResponse(
            self.session.post(
                'https://eu3-prod-direct.eurosportplayer.com/login',
                data=payload
            ).json()
        )
        return sessionTokenResponse.token()


    """
       SessionTokenResponse sends back an object containing the session token
    """
    class SessionTokenResponse(object):
        def __init__(self, data):
            self._data = data

        def token(self):
            return self._data.get('token', {})
