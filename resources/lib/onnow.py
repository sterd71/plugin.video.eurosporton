# -*- coding: utf-8 -*-

import sys
from xbmcplugin import addDirectoryItems, endOfDirectory
from resources.lib.common import build_list

"""
    List what's on Eurosport 1 first
"""    
def channel_schedule_key(video):
    attrs = video['attributes']

    if attrs.get('materialType') == 'LINEAR':
        channel = attrs.get('path')
        if 'eurosport-1' in channel:
            return 1
        if 'eurosport-2' in channel:
            return 2
        
    return attrs.get('scheduleStart')

"""
    Return list of programmes that are on now
"""    
def onnow_list(eurosport):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    onnow = eurosport.onnow()
    videos = onnow.videos()

    # Create list for items
    listing = []

    for video in sorted(videos, key=channel_schedule_key):
         build_list('onnow', video, listing, onnow)

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)


