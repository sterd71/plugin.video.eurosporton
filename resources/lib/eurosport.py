import datetime
import requests

from dateutil.parser import parse as parse_date
from dateutil import tz

ROOT_URL = 'https://eu3-prod-direct.eurosportplayer.com'

"""
  Eurosport object checks session token
  and returns the list of items available to watch now, or scheduled for later
"""
class Eurosport(object):
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()

        self.session.headers = {
            'cookie': 'st={}'.format(token),
            'X-disco-client': 'WEB:UNKNOWN:esplayer:prod',
            'X-disco-params': 'realm=eurosport,,'  
        }

    def ontv(self, collid, day):
        return OntvResponse(
            self.session.get(
                '{0}/cms/collections/{1}?include=default&{2}'.format(ROOT_URL,collid,day)
            ).json()
        )

    def onschedule(self):
        return OnscheduleResponse(
            self.session.get(
                '{}/cms/routes/schedule?include=default'.format(ROOT_URL)
            ).json()
        )
        
        
    def dailyList(self, collid, day):
        return DailyResponse(
            self.session.get(
                '{0}/cms/collections/{1}?include=default&{2}'.format(ROOT_URL,collid,day)
            ).json()
        )


    def ondemand(self):
        return OndemandResponse(
            self.session.get(
                '{}/cms/routes/on-demand?include=default'.format(ROOT_URL)
            ).json()
        )


    def sport(self, sport):
        return SportResponse(
            self.session.get(
                '{0}/cms/routes/sport/{1}?include=default'.format(ROOT_URL,sport)
            ).json()
        )

    def playback_info(self, video_id):
        return self.session.get(
            '{}/playback/v2/videoPlaybackInfo/{}?usePreAuth=true'.format(
                ROOT_URL,
                video_id
            )
        ).json()

    def olyonnow(self):
        return OntvResponse(
            self.session.get(
                '{0}/cms/routes/olympics/on-now?include=default'.format(ROOT_URL)
            ).json()
        )

    def olyonschedule(self):
        return OnscheduleResponse(
            self.session.get(
                '{0}/cms/routes/olympics/schedule?include=default'.format(ROOT_URL)
            ).json()
        )

    def olyontoday(self,collid,day,pageNumber):
        return DailyResponse(
            self.session.get(
              #  '{0}/cms/routes/olympics/schedule?include=default'.format(ROOT_URL)
              '{0}/cms/collections/{1}?include=default&{2}&page[items.number]={3}'.format(ROOT_URL,collid,day,pageNumber)
            ).json()
        )

"""
    OntvResponse sends back a list of videos that have a start time before now and
    and end time after now
"""    
class OntvResponse(object):
    def __init__(self, data):
        self._data = data

    def videos(self, onlyAvailable=True):

        def filterMethod(o):
            
            if o.get('type') != 'video':
                return False
            if not onlyAvailable:
                return True

            attributes = o.get('attributes', {})

            # Exclude items not on a channel
            materialType = attributes.get('materialType')
            if materialType != 'LINEAR':
                return False

            # Only include items that are on now
            if len(attributes) > 0:
                av_start = parse_date(attributes['scheduleStart'])
                av_end = parse_date(attributes['scheduleEnd'])
                now = datetime.datetime.now(tz.tzutc())
                return av_start <= now <= av_end

            return False

        return filter(
            filterMethod,
            self._data.get('included', [])
        )

        
"""
    OnscheduleResponse sends back an object containing an id and an array of dates inthe current schedule
"""
class OnscheduleResponse(object):
    def __init__(self, data):
        self._data = data

    def scheduleCollection(self, onlyAvailable=True):

        def filterMethod(o):
            if o.get('type') != 'collection':
                return False
            if not onlyAvailable:
                return True
                
            return True    

        return filter(
            filterMethod,
            self._data.get('included', [])
        )

    def images(self):
        return filter(
            lambda o: o.get('type') == 'image',
            self._data.get('included', [])
        )

    def get_image_url(self, id):
        wanted_images = list(
            filter(
                lambda i: i['id'] == id,
                self.images()
            )
        )
        if len(wanted_images) > 0:
            return wanted_images[0]['attributes'].get('src')
        return None

        
        
"""
    OndemandResponse sends back a list of sports that have videos available
"""
class OndemandResponse(object):
    def __init__(self, data):
        self._data = data

    def sports(self, onlyAvailable=True):

        def filterMethod(o):

            if o.get('type') != 'taxonomyNode':
                return False
            if not onlyAvailable:
                return True
                
            return True    

        return filter(
            filterMethod,
            self._data.get('included', [])
        )

    def images(self):
        return filter(
            lambda o: o.get('type') == 'image',
            self._data.get('included', [])
        )

    def get_image_url(self, id):
        wanted_images = list(
            filter(
                lambda i: i['id'] == id,
                self.images()
            )
        )
        if len(wanted_images) > 0:
            return wanted_images[0]['attributes'].get('src')
        return None



"""
    SportResponse sends back a list of on demand videos that have a start time before now and
    and end time after now
"""    
class SportResponse(object):
    def __init__(self, data):
        self._data = data

    def videos(self, onlyAvailable=True):

        def filterMethod(o):

            if o.get('type') != 'video':
                return False
            if not onlyAvailable:
                return True

            availability = o.get('attributes', {}).get('availabilityWindows', [])
            if len(availability) > 0:
                av_window = availability[0]
                av_start = parse_date(av_window['playableStart'])
                av_end = parse_date(av_window['playableEnd'])
                now = datetime.datetime.now(tz.tzutc())
                return av_start <= now <= av_end

            return False

        return filter(
            filterMethod,
            self._data.get('included', [])
        )

    def images(self):
        return filter(
            lambda o: o.get('type') == 'image',
            self._data.get('included', [])
        )

    def get_image_url(self, id):
        wanted_images = list(
            filter(
                lambda i: i['id'] == id,
                self.images()
            )
        )
        if len(wanted_images) > 0:
            return wanted_images[0]['attributes'].get('src')
        return None


"""
    DailyResponse sends back a list of videos that are showing on the selected day
"""    
class DailyResponse(object):
    def __init__(self, data):
        self._data = data

    def videos(self, onlyAvailable=True):

        def filterMethod(o):

            if o.get('type') != 'video':
                return False
            if not onlyAvailable:
                return True

            return True

        return filter(
            filterMethod,
            self._data.get('included', [])
        )

    def images(self):
        return filter(
            lambda o: o.get('type') == 'image',
            self._data.get('included', [])
        )

    def get_image_url(self, id):
        wanted_images = list(
            filter(
                lambda i: i['id'] == id,
                self.images()
            )
        )
        if len(wanted_images) > 0:
            return wanted_images[0]['attributes'].get('src')
        return None

