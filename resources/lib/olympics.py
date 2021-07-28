import sys
from datetime import datetime
import time
from xbmcplugin import addDirectoryItems, endOfDirectory
from xbmcgui import ListItem
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
    Sort by date
"""
def date_sort_key(options):
    return options.get('value')


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
def olympics_ontoday(eurosport,collid,day):

    # Set up list
    pageNumber = 1

    olympics_pager(eurosport, collid, day, pageNumber)
    

"""
    Return a page of videos
"""    
def olympics_pager(eurosport, collid, day, pageNumber):

    # Get the plugin handle
    __handle__ = int(sys.argv[1])

    nextPage = False
            
    # Fudge eurosport page number   
    if int(pageNumber) == 1 or int(pageNumber) == 2:
        euroPageNumber = 1
    if int(pageNumber) == 3 or int(pageNumber) == 4:
        euroPageNumber = 2
    if int(pageNumber) == 5 or int(pageNumber) == 6:
        euroPageNumber = 3

    # Get videos for today & sort into transmission order
    response = eurosport.olyontoday(collid, day, euroPageNumber)
    videos = response.videos()
    sortedVideos = sorted(videos, key=schedule_start_key)

    # Set page limits
    if len(sortedVideos) == 0:
        start = 0
        end = 0
        nextPage = False
    else:     
        if int(pageNumber) % 2 != 0:
            start = 0
            end = 50
            if len(sortedVideos) > 50:
                nextPage = True
            else:
                nextPage = False
        else:
            if len(sortedVideos) == 100:
                start = 50
                end = 100
                nextPage = True
            else:
                start = 50
                end = len(sortedVideos)
                nextPage = False

    # Create subset of videos         
    subset = sortedVideos[start:end]

    # Create list for items
    listing = []

    for video in subset:
        build_list('daily', video, listing, response)

    if nextPage:
        __url__ = sys.argv[0]
        item = ListItem('Next')
        pageNumber = int(pageNumber) + 1
        url = '{0}?action=OlympicsPager&collid={1}&day={2}&pageNumber={3}'.format(__url__, collid, day, pageNumber)
        isfolder = True
        listing.append((url, item, isfolder))
        
    addDirectoryItems(__handle__, listing, len(listing))

    
    endOfDirectory(__handle__)




"""
    Return list of on available dates
"""    
def olympics_schedule(eurosport):

    # Get the plugin url
    __url__ = sys.argv[0]

    # Get the plugin handle
    __handle__ = int(sys.argv[1])

    onschedule = eurosport.olyonschedule()
    schedule_collection = onschedule.scheduleCollection()

    # Create list for items
    listing = []

    # Get todays date
    date_today = datetime.today().strftime('%Y-%m-%d')
    
    for schedule in schedule_collection:

        try:
            # Collection Id
            collection_id = schedule.get('id')

            attrs = schedule['attributes']
            
            component = attrs.get('component')
            filters = component.get('filters')

            for schedule_filter in filters:
                options = schedule_filter.get('options')
                for option in options:
                    schedule_str = option.get('value')
                    try:
                        schedule_date = datetime.strptime(schedule_str, '%Y-%m-%d')   
                    except TypeError:
                        schedule_date = datetime(*(time.strptime(schedule_str, '%Y-%m-%d')[0:6]))
                    schedule_format = '%d %B'
                    if schedule_str == date_today:
                        title = '[B][COLOR red]' + schedule_date.strftime(schedule_format) + '[/COLOR][/B]'
                    else:
                        title = schedule_date.strftime(schedule_format)
                    parameter = option.get('parameter')
                    item = ListItem(title)
                    labels = {'title': title, 'sorttitle': title}
                    item.setInfo('video', labels)
                    url = '{0}?action=Olympics: On today&collid={1}&day={2}'.format(__url__, collection_id, parameter)   
                    isfolder = True
                    # Add item to our listing
                    listing.append((url, item, isfolder))
        except:    
            pass

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)

"""
    Return todays collection id
"""    
def getcollectionid(eurosport):

    # Get the plugin url
    __url__ = sys.argv[0]

    # Get the plugin handle
    __handle__ = int(sys.argv[1])

    onschedule = eurosport.onschedule()
    schedule_collection = onschedule.scheduleCollection()

    
    for schedule in schedule_collection:

        try:
            # Collection Id
            collection_id = schedule.get('id')
        except:    
            pass

    return collection_id

    

