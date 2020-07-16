# -*- coding: utf-8 -*-

import routing
import logging
import requests
import simplejson
import xbmcaddon
from resources.lib import kodiutils, kodilogging
from resources.lib.eurosport import Eurosport
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setContent, setResolvedUrl


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

token = ADDON.getSetting('eurosport-token')
logger.info('Using token: {}'.format(token))
e = Eurosport(token)


def video_sort_key(video):
    attrs = video['attributes']
    
    return attrs.get('scheduleStart')


@plugin.route('/')
def index():

    setContent(plugin.handle, 'videos')

    schedule = e.schedule()
    videos = schedule.videos()

    #import web_pdb; web_pdb.set_trace()

    for video in sorted(videos, key=video_sort_key):
        attrs = video['attributes']

        ## Add extra detail to program titles
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
            image_url = schedule.get_image_url(images[0]['id'])
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

        item.setInfo('Video', labels)

        item.setProperty('IsPlayable', 'true')
        item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'hls')

        addDirectoryItem(
            plugin.handle,
            plugin.url_for(
                play_video,
                id=video['id']
            ),
            item,
            False,
            len(videos)
        )

    endOfDirectory(plugin.handle)


@plugin.route('/play')
def play_video():
    video_id = plugin.args['id'][0]

    playback_info = e.playback_info(video_id)
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
    setResolvedUrl(plugin.handle, True, listitem=play_item)


def run():
    plugin.run()
