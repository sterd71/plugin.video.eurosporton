# -*- coding: utf-8 -*-

import datetime

import sys
import logging
import xbmcaddon
from resources.lib import kodilogging
from resources.lib.eurosport import Eurosport
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItems, endOfDirectory, setResolvedUrl


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()


def sport_sort_key(sport):
    attrs = sport['attributes']
    
    return attrs.get('name')

"""
    Return list of on demand sports
"""    
def ondemand_list(token):

    # Get the plugin url
    __url__ = sys.argv[0]

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    

    
    # Get eurosport response
    e = Eurosport(token)
    
    ondemand = e.ondemand()
    sports = ondemand.sports()

    # Create list for items
    listing = []

    for sport in sorted(sports, key=sport_sort_key):
        attrs = sport['attributes']

        title = attrs.get('name')
        alternateTitle = attrs.get('alternateId')

        list_item = ListItem(label=title)

        images = sport.get(
            'relationships', {}
        ).get(
            'images', {}
        ).get(
            'data', []
        )

        if len(images) > 0:
            image_url = ondemand.get_image_url(images[0]['id'])
            list_item.setArt({
                'thumb': image_url,
                'icon': image_url
            })

        list_item.setInfo('video',  {'title': title})

        list_item.setProperty('IsPlayable', 'false')
        
        url = '{0}?action=Select sport&token={1}&sport={2}'.format(__url__, token, alternateTitle)   

        # is_folder is set to true as this will be a list of sports
        isfolder = True
        
        # Add item to our listing
        listing.append((url, list_item, isfolder))

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)


