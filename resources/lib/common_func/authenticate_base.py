import xbmcaddon
from resources.lib.network.realm_base import Realm
from resources.lib.network.token_base import Token
from resources.lib.network.arkosesitekey_base import ArkoseSiteKey
from resources.lib.network.arkosetoken_base import ArkoseToken
from resources.lib.network.sessiontoken_base import SessionToken

"""
  Authenticate logs into the Eurosport service and stores the session token
"""
class Authenticate(object):
    def __init__(self,settings):
        self.realm = Realm().getRealm()
        self.token = Token(self.realm).getToken()
        self.arkoseSiteKey = ArkoseSiteKey(self.realm, self.token).getArkoseSiteKey()
        self.arkoseToken = ArkoseToken(self.arkoseSiteKey).getArkoseToken()
        self.sessionToken = SessionToken(settings.username, settings.password, self.realm, self.arkoseSiteKey, self.arkoseToken).getSessionToken()
        myrealm = self.realm
        mytoken = self.token
        mysitekey = self.arkoseSiteKey
        myarktoken = self.arkoseToken
        mysessiontoken = self.sessionToken
        stop = "test"

    def getToken(self):
        return self.token
