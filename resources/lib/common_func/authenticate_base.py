import xbmcaddon
from resources.lib.network.realm_base import Realm
from resources.lib.network.token_base import Token

ROOT_URL = 'https://eu3-prod-direct.eurosportplayer.com'

"""
  Authenticate logs into the Eurosport service and stores the session token
"""
class Authenticate(object):
    def __init__(self,settings):
        self.realm = Realm().getRealm()
        self.token = Token(self.realm).getToken()
        mytoke = self.token
        stop = "test"

    def getToken(self):
        return self.token


    def getArkoseSiteKey(self):
        return ArkoseSiteKeyResponse(
            self.session.get(
                '{}/cms/configs/auth'.format(ROOT_URL)
            ).json()
        )


    """
    OnscheduleResponse sends back an object containing an id and an array of dates inthe current schedule
    """
    class ArkoseSiteKeyResponse(object):
        def __init__(self, data):
            self._data = data

            def siteKey(self, onlyAvailable=True):

                def filterMethod(o):
                    if o.get('type') != 'collection':
                        return False
                    if not onlyAvailable:
                        return True
                
                    return True    

                return filter(
                    filterMethod,
                    self._data.get('included', [])
                )
