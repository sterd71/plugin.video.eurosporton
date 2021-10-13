import requests

"""
  ArkoseToken fetches the Eurosport token from Arkose authentication service
"""
class ArkoseToken(object):
    def __init__(self,arkoseSiteKey):
        self.session = requests.Session()
        self.arkoseToken = self.setArkoseToken(arkoseSiteKey)

        
    def getArkoseToken(self):
        return self.arkoseToken


    def setArkoseToken(self,arkoseSiteKey):
        payload = {'public_key' : '{}'.format(arkoseSiteKey)}
        arkoseTokenResponse = self.ArkoseTokenResponse(
            self.session.post(
                'https://client-api.arkoselabs.com/fc/gt2/public_key/{}'.format(arkoseSiteKey),
                data=payload
            ).json()
        )
        return arkoseTokenResponse.token()


    """
       ArkoseTokenResponse sends back an object containing the Arkose token
    """
    class ArkoseTokenResponse(object):
        def __init__(self, data):
            self._data = data

        def token(self):
            return self._data.get('token', {})
