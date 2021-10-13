import requests

"""
  ArkoseSiteKey fetches the Eurosport site key from Arkose authentication service
"""
class ArkoseSiteKey(object):
    def __init__(self,realm,token):
        self.session = requests.Session()
        self.session.headers = {
            'cookie': 'st={}'.format(token),
            'X-disco-params': 'realm=' + realm + ',,'  
        }
        self.arkoseSiteKey = self.setArkoseSiteKey()

        
    def getArkoseSiteKey(self):
        return self.arkoseSiteKey


    def setArkoseSiteKey(self):    
        arkoseSiteKeyResponse = self.ArkoseSiteKeyResponse(
            self.session.get(
                'https://eu3-prod-direct.eurosportplayer.com/cms/configs/auth'
            ).json()
        )
        return arkoseSiteKeyResponse.sitekey()


    """
       ArkoseSiteKeyResponse sends back an object containing the Arkose site key
    """
    class ArkoseSiteKeyResponse(object):
        def __init__(self, data):
            self._data = data

        def sitekey(self):
            return self._data.get('data', {}).get('attributes', {}).get('config', {}).get('arkoseSiteKeys', {}).get('loginForm', {})


