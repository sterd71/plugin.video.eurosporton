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
    scheduleCollection = onschedule.scheduleCollection()

    # Create list for items
    listing = []
    

    #for schedule in sorted(scheduleCollection, key=name_sort_key):
    for schedule in scheduleCollection:    	
    	
        try:        
            # Collection Id
            collectionId = schedule.get('id')

            attrs = schedule['attributes']
            
            component = attrs.get('component')
            filters = component.get('filters')

            for scheduleFilter in filters:
            	 options = scheduleFilter.get('options')
            	 for option in options:
                    scheduleStr = option.get('value')
                    scheduleDate = datetime.strptime(scheduleStr, '%Y-%m-%d')   
                    format = '%d %B'
                    title = scheduleDate.strftime(format)  
                    parameter = option.get('parameter')
                    item = ListItem(title)
                    labels = {'title': title, 'sorttitle': title}
                    item.setInfo('video', labels)
                    url = '{0}?action=Select date&collid={1}&day={2}'.format(__url__, collectionId, parameter)   
                    isfolder = True
                    # Add item to our listing
                    listing.append((url, item, isfolder))
        except:    
            pass

    addDirectoryItems(__handle__, listing, len(listing))

    endOfDirectory(__handle__)


