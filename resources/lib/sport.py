# -*- coding: utf-8 -*-

import sys
import logging
import xbmcaddon
from resources.lib import kodilogging
from resources.lib.eurosport import Eurosport
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItems, endOfDirectory


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
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
def sport_list(token,sport):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    # Get eurosport response
    e = Eurosport(token)
        
    sport = e.sport(sport)
    videos = sport.videos()

    # Create list for items
    listing = []

    if sortOrder == "Ending soon":
        for video in sorted(videos, key=publish_end_key):
            build_list(video, listing, sport)
    elif sortOrder == 'Earliest first':
        for video in sorted(videos, key=publish_start_key):
            build_list(video, listing, sport)
    else:    	
        for video in sorted(videos, key=publish_start_key, reverse=True):
            build_list(video, listing, sport)
		
    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)

def build_list(video, listing, sport):

    # Get the plugin url
    __url__ = sys.argv[0]

    try:        
        attrs = video['attributes']

        # Format programme  titles
        title = attrs.get('name')

        item = ListItem(title)

        images = video.get(
            'relationships', {}
        ).get(
            'images', {}
        ).get(
            'data', []
        )

        if len(images) > 0:
            image_url = sport.get_image_url(images[0]['id'])
            item.setArt({
                'thumb': image_url,
                'icon': image_url
            })

        # Format the publishStart date
        publishStart = str(attrs.get('publishStart')[:10])
        
        # Get the plot
        plot = attrs.get('description')
        if plot == '' or plot is None:
            plot = attrs.get('secondaryTitle')

        labels = {
            'title': title,
            'plot': plot,
            'premiered': publishStart,
            'aired': publishStart,
            'mediatype': 'video'
        }

        item.setInfo('video', labels)

        item.setProperty('IsPlayable', 'true')
        item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'hls')

        id = video.get('id')
        url = '{0}?action=play&id={1}'.format(__url__, id)
    
        # is_folder is set to false as there is no sublist 
        isfolder = False
    
        # Add item to our listing
        listing.append((url, item, isfolder))
    except:    
        pass
