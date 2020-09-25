# -*- coding: utf-8 -*-


import sys
from xbmcplugin import addDirectoryItems, endOfDirectory
from resources.lib.common import build_list

def sport_sort_key(sport):
    attrs = sport['attributes']
    
    return attrs.get('name')

"""
    Return list of on demand sports
"""    
def ondemand_list(eurosport):
    
    # Get the plugin handle
    __handle__ = int(sys.argv[1])

    ondemand = eurosport.ondemand()
    sports = ondemand.sports()

    # Create list for items
    listing = []

    for sport in sorted(sports, key=sport_sort_key):
         build_list('ondemand', sport,  listing, ondemand)

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)


