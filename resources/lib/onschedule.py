# -*- coding: utf-8 -*-


import sys
from datetime import datetime
from xbmcplugin import addDirectoryItems, endOfDirectory
from xbmcgui import ListItem


def name_sort_key(schedule):
    attrs = schedule['attributes']
    
    return attrs.get('name')


def date_sort_key(options):
    return options.get('value')

"""
    Return list of on available dates
"""    
def onschedule_list(eurosport):

    # Get the plugin url
    __url__ = sys.argv[0]

    # Get the plugin handle
    __handle__ = int(sys.argv[1])

    onschedule = eurosport.onschedule()
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
                    schedule_date = datetime.strptime(schedule_str, '%Y-%m-%d')   
                    schedule_format = '%d %B'
                    if schedule_str == date_today:
                        title = '[B][COLOR red]' + schedule_date.strftime(schedule_format) + '[/COLOR][/B]'
                    else:
                        title = schedule_date.strftime(schedule_format)
                    parameter = option.get('parameter')
                    item = ListItem(title)
                    labels = {'title': title, 'sorttitle': title}
                    item.setInfo('video', labels)
                    url = '{0}?action=Select date&collid={1}&day={2}'.format(__url__, collection_id, parameter)   
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

