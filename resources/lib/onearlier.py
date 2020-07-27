# -*- coding: utf-8 -*-

import sys
from xbmcplugin import addDirectoryItems, endOfDirectory
from resources.lib.common import build_list

"""
    Sort by start time
"""    
def schedule_start_key(video):
    attrs = video['attributes']
    return attrs.get('scheduleStart')

"""
    Return list of programmes that were on earlier
"""    
def onearlier_list(eurosport):
    
    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    onearlier = eurosport.onearlier()
    videos = onearlier.videos()

    # Create list for items
    listing = []

    for video in sorted(videos, key=schedule_start_key):
         build_list('onearlier', video, listing, onearlier)

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)
