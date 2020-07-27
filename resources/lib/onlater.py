# -*- coding: utf-8 -*-

import sys
from xbmcplugin import addDirectoryItems, endOfDirectory
from resources.lib.common import build_list

def schedule_start_key(video):
    attrs = video['attributes']
    return attrs.get('scheduleStart')

"""
    Return list of programmes that are on later
"""    
def onlater_list(eurosport):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    onlater = eurosport.onlater()
    videos = onlater.videos()

    # Create list for items
    listing = []

    for video in sorted(videos, key=schedule_start_key):
        build_list('onlater', video, listing, onlater)

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)


