# -*- coding: utf-8 -*-

import sys
import logging
from urlparse import parse_qsl
import xbmcaddon
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItems, endOfDirectory, setContent, setResolvedUrl
from resources.lib.eurosport import Eurosport
from resources.lib.onschedule import onschedule_list
from resources.lib.ondemand import ondemand_list
from resources.lib.sport import sport_list
from resources.lib.daily import daily_list
from resources.lib.ontv import ontv_list
from resources.lib.olympics import olympics_onnow
from resources.lib.olympics import olympics_schedule
from resources.lib.olympics import olympics_ontoday
from resources.lib.olympics import olympics_pager


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

token = ADDON.getSetting('eurosport-token')
logger.info('Using token: {}'.format(token))
eurosport = Eurosport(token)

# Get the plugin url
__url__ = sys.argv[0]

# Get the plugin handle
__handle__ = int(sys.argv[1])

"""
Router function that calls other functions depending on the provided paramstring
:param paramstring:
:return:
"""
def router(paramstring):

    setContent(__handle__, 'videos')

    # Parse a URL-encoded paramstring
    params = dict(parse_qsl(paramstring[1:]))  
    
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'On TV':
          ontv_list(eurosport)
        if params['action'] == 'On schedule':
          onschedule_list(eurosport)
        if params['action'] == 'Select date':
          daily_list(eurosport, params['collid'],params['day'])
        if params['action'] == 'On demand':
          ondemand_list(eurosport)
        if params['action'] == 'Select sport':
          sport_list(eurosport, params['sport'])
        if params['action'] == 'play':
          play_video(params['id'])
        if params['action'] == 'Olympics: On now':
          olympics_onnow(eurosport)
        if params['action'] == 'Olympics: On schedule':
          olympics_schedule(eurosport)
        if params['action'] == 'Olympics: On today':
          olympics_ontoday(eurosport, params['collid'],params['day'])
        if params['action'] == 'OlympicsPager':
          olympics_pager(eurosport, params['collid'],params['day'],params['pageNumber'])
    else:
        # If no parameters - then display the top menu
        list_topMenu()  


"""
Create the top menu
:return: None
"""
def list_topMenu():

    # Get list of menu items
    menuItems = get_topMenu()
  
    # Create list for menu items
    listing = []
  
    for menuItem in menuItems:
        # Add an item with just the text
        list_item = ListItem(label=menuItem)
        list_item.setInfo('video', {'title': menuItem})
        url = '{0}?action={1}'.format(__url__, menuItem)
        is_folder = True
        listing.append((url, list_item, is_folder))
  
    addDirectoryItems(__handle__, listing, len(listing))
    endOfDirectory(__handle__)
  
"""
Get the list of top menu items
:return: list
"""
def get_topMenu():
    listing = []
    listing.append('Olympics: On now')
    listing.append('Olympics: On schedule')
    listing.append('On TV')
    listing.append('On schedule')
    listing.append('On demand')
    return listing  

"""
Play video located at the URL
"""
def play_video(id):
        
    ADDON = xbmcaddon.Addon()
    streamType = ADDON.getSetting('streamType')
    playback_info = eurosport.playback_info(id)

    if streamType == 'hls':
        stream_url = playback_info.get(
            'data', {}
        ).get(
            'attributes', {}
        ).get(
            'streaming', {}
        ).get(
            'hls', {}
        ).get('url')

    if streamType == 'ism':
        stream_url = playback_info.get(
            'data', {}
        ).get(
            'attributes', {}
        ).get(
            'streaming', {}
        ).get(
            'mss', {}
        ).get('url')

    # Create a playable item with a path to play.
    play_item = ListItem(path=stream_url)
    # Pass the item to the Kodi player.
    setResolvedUrl(__handle__, True, listitem=play_item)
