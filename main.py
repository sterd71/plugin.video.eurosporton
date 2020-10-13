# -*- coding: utf-8 -*-

import sys
import xbmcaddon
from resources.lib import player

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this
ADDON = xbmcaddon.Addon()

if __name__ == '__main__':
    player.router(sys.argv[2])
    
