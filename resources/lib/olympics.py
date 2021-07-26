import sys
from datetime import datetime
from xbmcplugin import addDirectoryItems, endOfDirectory
from resources.lib.common import build_list
from resources.lib.onschedule import getcollectionid

"""
    List what's on Eurosport 1 first
"""    
def channel_schedule_key(video):
    attrs = video['attributes']

    #if attrs.get('materialType') == 'LINEAR':
    channel = attrs.get('path')
    if 'eurosport-1' in channel:
        return 1
    if 'eurosport-2' in channel:
        return 2
        
    return attrs.get('scheduleStart')


"""
    Sort videos by the scheduleStart timestamp
"""
def schedule_start_key(video):
    attrs = video['attributes']
    return attrs.get('scheduleStart')



"""
    Return list of programmes that are on now
"""    
def olympics_onnow(eurosport):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    

    olyonnow = eurosport.olyonnow()
    videos = olyonnow.videos()

    
    # Create list for items
    listing = []

    for video in sorted(videos, key=channel_schedule_key):
        build_list('ontv', video, listing, olyonnow)

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)



"""
    Return list of available videos for this day
"""    
def olympics_ontoday(eurosport):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])
    
    olyontoday = eurosport.olyontoday()
    videos = olyontoday.videos()

    # Create list for items
    listing = []

    for video in sorted(videos, key=schedule_start_key):
        build_list('daily', video, listing, olyontoday)
		
    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)
    
