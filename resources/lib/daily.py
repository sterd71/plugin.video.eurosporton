# -*- coding: utf-8 -*-

import sys
import xbmcaddon
from xbmcplugin import addDirectoryItems, endOfDirectory
from resources.lib.common import build_list

ADDON = xbmcaddon.Addon()
sortOrder = ADDON.getSetting('ondemand-sort-order')

"""
    Sort videos by the scheduleStart timestamp
"""
def schedule_start_key(video):
    attrs = video['attributes']
    return attrs.get('scheduleStart')

    


"""
    Return list of available videos for this day
"""    
def daily_list(eurosport,collid,day):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    dailyList = eurosport.dailyList(collid,day)
    videos = dailyList.videos()

    # Create list for items
    listing = []

    for video in sorted(videos, key=schedule_start_key):
        build_list('daily', video, listing, dailyList)
		
    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)
