# -*- coding: utf-8 -*-

import sys
import logging
from urlparse import parse_qsl
import xbmcaddon
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItems, endOfDirectory, setContent, setResolvedUrl
from resources.lib import kodilogging
from resources.lib.eurosport import Eurosport
from resources.lib.onearlier import onearlier_list
from resources.lib.onnow import onnow_list
from resources.lib.onlater import onlater_list
from resources.lib.ondemand import ondemand_list
from resources.lib.sport import sport_list


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

token = ADDON.getSetting('eurosport-token')
logger.info('Using token: {}'.format(token))
e = Eurosport(token)

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
        if params['action'] == 'On earlier':
          onearlier_list(params['token'])
        if params['action'] == 'On now':
          onnow_list(params['token'])
        if params['action'] == 'On later':
          onlater_list(params['token'])
        if params['action'] == 'On demand':
          ondemand_list(params['token'])
        if params['action'] == 'Select sport':
          sport_list(params['token'],params['sport'])
        if params['action'] == 'play':
          play_video(params['id'])
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
        url = '{0}?action={1}&token={2}'.format(__url__, menuItem, token)
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
    listing.append('On earlier')
    listing.append('On now')
    listing.append('On later')
    listing.append('On demand')
    return listing  

"""
Play video located at the URL
"""
def play_video(id):
        
    playback_info = e.playback_info(id)
    stream_url = playback_info.get(
        'data', {}
    ).get(
        'attributes', {}
    ).get(
        'streaming', {}
    ).get(
        'hls', {}
    ).get('url')

    # Create a playable item with a path to play.
    play_item = ListItem(path=stream_url)
    # Pass the item to the Kodi player.
    setResolvedUrl(__handle__, True, listitem=play_item)
