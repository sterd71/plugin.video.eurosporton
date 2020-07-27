# -*- coding: utf-8 -*-

import sys
import xbmcaddon
from xbmcplugin import addDirectoryItems, endOfDirectory
from resources.lib.common import build_list

ADDON = xbmcaddon.Addon()
sortOrder = ADDON.getSetting('ondemand-sort-order')

"""
    Sort videos by the publishStart timestamp
"""
def publish_start_key(video):
    attrs = video['attributes']
    return attrs.get('publishStart')
    
    
"""
    Sort videos by the publishEnd timestamp
"""
def publish_end_key(video):
    attrs = video['attributes']
    return attrs.get('publishEnd')
    


"""
    Return list of available videos for this sport
"""    
def sport_list(eurosport,sport):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    sport = eurosport.sport(sport)
    videos = sport.videos()

    # Create list for items
    listing = []

    if sortOrder == "Ending soon":
        for video in sorted(videos, key=publish_end_key):
            build_list('sport', video, listing, sport)
    elif sortOrder == 'Earliest first':
        for video in sorted(videos, key=publish_start_key):
            build_list('sport', video, listing, sport)
    else:    	
        for video in sorted(videos, key=publish_start_key, reverse=True):
            build_list('sport', video, listing, sport)
		
    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)
