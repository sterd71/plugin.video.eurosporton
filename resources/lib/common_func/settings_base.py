import xbmcaddon

"""
  Settings object loads in the values from settings.xml at runtime
"""
class Settings(object):
    def __init__(self):
        ADDON = xbmcaddon.Addon()
        self.username = ADDON.getSetting('username')
        self.password = ADDON.getSetting('password')


    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password
