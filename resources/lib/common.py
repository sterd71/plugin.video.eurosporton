# -*- coding: utf-8 -*-

from dateutil.parser import parse as parse_date
from dateutil import tz

import sys
import urllib
import xbmcaddon
from xbmcgui import ListItem

def build_list(type, video, listing, response):

    ADDON = xbmcaddon.Addon()
    engine = ADDON.getSetting('engine')
    streamType = ADDON.getSetting('streamType')

    # Get the plugin url
    __url__ = sys.argv[0]

    try:        
        attrs = video['attributes']
        alternateTitle = attrs.get('alternateId')
        
        if type == 'onlater':
            # Pull start time from availability window
            availability = video.get('attributes', {}).get('availabilityWindows', [])
            if len(availability) > 0:
                av_window = availability[0]
                av_start = parse_date(av_window['playableStart'])
                av_startlocal = av_start.astimezone(tz.tzlocal())
                av_startstr = av_startlocal.strftime("%H:%M")
            
            title = av_startstr + ' - ' + attrs.get('name')
        else:    
            # Set the base title
            title = attrs.get('name')
        
        # Add chanel details for on-air shows
        if type == 'onearlier' or type == 'onnow' or type == 'onlater':
            if attrs.get('materialType') == 'LINEAR':
                channel = attrs.get('path')
                if 'eurosport-1' in channel:
                    title = title + ' - (E1)'
                if 'eurosport-2' in channel:
                    title = title + ' - (E2)'

            if attrs.get('broadcastType') == 'LIVE':
                title = title + ' (Live)'

        item = ListItem(title)

        # Get image and it's url
        images = video.get(
            'relationships', {}
        ).get(
            'images', {}
        ).get(
            'data', []
        )

        if len(images) > 0:
            image_url = response.get_image_url(images[0]['id'])
            item.setArt({
                'thumb': image_url,
                'icon': image_url
            })

        # Set the premiered date
        if type == 'onearlier' or  type == 'onnow' or type =='onlater':
            premiered = str(attrs.get('scheduleStart')[:10])
            timestamp = attrs.get('scheduleStart')
        
        if type == 'sport':
            premiered = str(attrs.get('publishStart')[:10])
            timestamp = attrs.get('publishStart')
        
        # Get the plot
        plot = attrs.get('description')
        if plot == '' or plot is None:
            plot = attrs.get('secondaryTitle')

        # Set the metadata
        if type == 'ondemand':
            labels = {
                'title': title,
                'sorttitle': title 
            }
        else:    
            labels = {
                'title': title,
                'sorttitle': title, 
                'plot': plot,
                'premiered': premiered,
                'aired': premiered,
                'dateadded': timestamp,
                'mediatype':'episode'
            }

        item.setInfo('video', labels)

        if type == 'onlater' or type == 'ondemand':
            item.setProperty('IsPlayable', 'false')
        else:    
            item.setProperty('IsPlayable', 'true')

        #import web_pdb; web_pdb.set_trace()

        # Ondemand brings up a list of items to select, not play            
        if type == 'ondemand':
            url = '{0}?action=Select sport&sport={1}'.format(__url__, alternateTitle)   
            isfolder = True
        else:    
            # Determine which stream to play
            if engine == 'inputstream.adaptive' and streamType == 'hls':
                item.setMimeType('application/x-mpegURL')
                item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                item.setProperty('inputstream.adaptive.manifest_type', 'hls')
            
            elif engine == 'ffmpeg' and streamType == 'hls':
                item.setMimeType('application/x-mpegURL')
                item.setProperty('inputstreamclass', 'inputstream.ffmpegdirect')
                item.setProperty('inputstream.ffmpegdirect.manifest_type', 'hls,applehttp')
                item.setProperty('inputstream.ffmpegdirect.is_realtime_stream', 'true')
                if type == 'ondemand':
                    item.setProperty('inputstream.ffmpegdirect.stream_mode', 'catchup')
                    item.setProperty('inputstream.ffmpegdirect.open_mode', 'ffmpeg')
                    item.setProperty('inputstream.ffmpegdirect.playback_as_live', 'true')

            elif engine == 'inputstream.adaptive' and streamType == 'ism':
                item.setMimeType('text/xml')
                item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                item.setProperty('inputstream.adaptive.manifest_type', 'ism')
            
            elif engine == 'ffmpeg' and streamType == 'ism':
                item.setProperty('inputstreamclass', 'inputstream.ffmpegdirect')
                item.setProperty('inputstream.ffmpegdirect.manifest_type', 'ism')
                item.setProperty('inputstream.ffmpegdirect.is_realtime_stream', 'true')
                if type == 'ondemand':
                    item.setProperty('inputstream.ffmpegdirect.stream_mode', 'catchup')
                    item.setProperty('inputstream.ffmpegdirect.open_mode', 'ffmpeg')
                    item.setProperty('inputstream.ffmpegdirect.playback_as_live', 'true')
            
            id = video.get('id')
            url = '{0}?action=play&id={1}'.format(__url__, id)
            isfolder = False
    
        # Add item to our listing
        listing.append((url, item, isfolder))
    except:    
        pass
