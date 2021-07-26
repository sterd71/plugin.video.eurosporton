# -*- coding: utf-8 -*-

import sys

import datetime
from dateutil.parser import parse as parse_date
from dateutil import tz

import xbmc
import xbmcaddon
from xbmcgui import ListItem


def getKodiVersion():
    return xbmc.getInfoLabel("System.BuildVersion").split(".")[0]

def build_list(type, video, listing, response):

    ADDON = xbmcaddon.Addon()
    engine = ADDON.getSetting('engine')
    streamType = ADDON.getSetting('streamType')
    kodi_version = int(getKodiVersion())

    # Get the plugin url
    __url__ = sys.argv[0]


    try:
        attrs = video['attributes']
        alternateTitle = attrs.get('alternateId')

        if type == 'sport':
            # Pull start time from availability window
            availability = video.get('attributes', {}).get('availabilityWindows', [])
            if len(availability) > 0:
                av_window = availability[0]
                av_start = parse_date(av_window['playableStart'])
                av_start_local = av_start.astimezone(tz.tzlocal())
                av_startstr = av_start_local.strftime("%H:%M")
            
            title = av_startstr + ' - ' + attrs.get('name')
        elif type == 'daily':
            # Pull start time from schedule start
            av_start = parse_date(attrs['scheduleStart'])
            av_start_local = av_start.astimezone(tz.tzlocal())
            av_startstr = av_start_local.strftime("%H:%M")
            
            title = av_startstr + ' - ' + attrs.get('name')
        elif type == 'ontv':
            # Pull start time from schedule start
            av_start = parse_date(attrs['scheduleStart'])
            av_start_local = av_start.astimezone(tz.tzlocal())
            channel = attrs.get('path')
            if 'eurosport-1' in channel:
                title = 'Eurosport 1: ' + attrs.get('name')
            if 'eurosport-2' in channel:
                title = 'Eurosport 2: ' + attrs.get('name')
            
        else:
            # Set the base title
            title = attrs.get('name')
        
        # Add chanel details for on-air shows
        if type == 'daily':
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
            try: 
                image_url = response.get_image_url(images[0]['id'])
                item.setArt({
                    'thumb': image_url,
                    'icon': image_url
                })
            except:
                pass

        # Set the premiered date
        if type == 'daily' or type == 'ontv':
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

        if type == 'ondemand':
            isPlayable = 'false'
        else:
            now = datetime.datetime.now(tz.tzutc())
            if av_start_local > now:
                isPlayable = 'false'
            else:
                isPlayable = 'true'
        
        item.setProperty('IsPlayable', isPlayable)

        # Ondemand brings up a list of items to select, not play
        if type == 'ondemand':
            url = '{0}?action=Select sport&sport={1}'.format(__url__, alternateTitle)
            isfolder = True
        else:
            # Determine which stream to play

            # Initialise properties
            mimetype = ''
            inputstreamtype = ''
            manifesttype = ''
            inputstream = ''
            manifest = ''

            
            # Matrix or earlier?
            if kodi_version > 18:
                inputstream = 'inputstream'
            else:
                if engine == 'inputstream.adaptive':
                    inputstream = 'inputstreamaddon'
                if engine == 'ffmpeg':
                    inputstream = 'inputstreamclass'

            # Set manifest & inputstream type
            if engine == 'inputstream.adaptive':
                manifest = 'inputstream.adaptive.manifest_type'
                inputstreamtype = 'inputstream.adaptive'
            if engine == 'ffmpeg':
                manifest = 'inputstream.ffmpegdirect.manifest_type'
                inputstreamtype = 'inputstream.ffmpegdirect'
                item.setProperty('inputstream.ffmpegdirect.is_realtime_stream', 'true')

            # Override settings for HLS streams
            if streamType == 'hls':
                mimetype = 'application/x-mpegURL'
                manifesttype = 'hls'

            # Override settings for ISM streams
            if streamType == 'ism':
                mimetype = 'text/xml'
                manifesttype = 'ism'


            # Set properties
            item.setContentLookup(False)
            item.setProperty(inputstream, inputstreamtype)
            item.setProperty(manifest, manifesttype)
            if (len(mimetype) != 0):
                item.setMimeType(mimetype)

           
            # Extra properties for ism ondemand streams
            if type == 'ondemand' and streamType == 'ism' :
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

