# -*- coding: utf-8 -*-

import sys
#import routing
import logging
#import requests
#import simplejson
import xbmcaddon
from resources.lib import kodilogging
from resources.lib.eurosport import Eurosport
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItems, endOfDirectory, setResolvedUrl


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()


def video_sort_key(video):
    attrs = video['attributes']
    
    return attrs.get('scheduleStart')

"""
    Return list of programmes that are on now
"""    
def onnow_list(token):

    # Get the plugin url
    __url__ = sys.argv[0]

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    # Get eurosport response
    e = Eurosport(token)
    
    onnow = e.onnow()
    videos = onnow.videos()

    # Create list for items
    listing = []

    for video in sorted(videos, key=video_sort_key):
        attrs = video['attributes']

        # Format programme  titles
        title = attrs.get('name')

        if attrs.get('materialType') == 'LINEAR':
            channel = attrs.get('path')
	    if 'eurosport-1' in channel:
	        title = title + ' - (E1)'
	    if 'eurosport-2' in channel:
	        title = title + ' - (E2)'
		
    	if attrs.get('broadcastType') == 'LIVE':
    	    title = title + ' (Live)'


        item = ListItem(title)

        images = video.get(
            'relationships', {}
        ).get(
            'images', {}
        ).get(
            'data', []
        )

        if len(images) > 0:
            image_url = onnow.get_image_url(images[0]['id'])
            item.setArt({
                'thumb': image_url,
                'icon': image_url
            })

        labels = {
            'title': title,
            'plot': attrs.get('description'),
            'premiered': attrs.get('scheduleStart'),
    	    'aired': attrs.get('scheduleStart'),
            'mediatype': 'video'
        }

        item.setInfo('video', labels)

        item.setProperty('IsPlayable', 'true')
        item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        
        
        playback_info = e.playback_info(video['id'])
        stream_url = playback_info.get(
            'data', {}
        ).get(
            'attributes', {}
        ).get(
            'streaming', {}
        ).get(
            'hls', {}
        ).get('url')
        
        url = '{0}?action=play&video={1}'.format(__url__, stream_url)
        
        # is_folder is set to false as there is no sublist 
        isfolder = False
        
        # Add item to our listing
        listing.append((url, item, isfolder))

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)


