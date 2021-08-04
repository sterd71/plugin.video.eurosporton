import logging
import xbmcaddon


"""
  Logger object provides API to output messages to Kodi log
"""
class ESLogger(object):
    def __init__(self):
        ADDON = xbmcaddon.Addon()
        logger = logging.getLogger(ADDON.getAddonInfo('id'))

    def loginfo(self, message):
        self.logger.info(message)

