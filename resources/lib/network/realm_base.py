import requests

"""
  Realm fetches and stores the site realm
"""
class Realm(object):
    def __init__(self):
        self.session = requests.Session()
        self.realm = self.setRealm()

        
    def getRealm(self):
        return self.realm


    def setRealm(self):    
        realmResponse = self.RealmResponse(
            self.session.get(
                'https://prod-realmservice.mercury.dnitv.com/realm-config/www.eurosportplayer.com'
            ).json()
        )
        return realmResponse.realm()


    """
    RealmResponse sends back an object containing the Eurosport realm
    """
    class RealmResponse(object):
        def __init__(self, data):
            self._data = data

        def realm(self):
            return self._data.get('realm', [])
            
