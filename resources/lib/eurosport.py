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
            'cookie': 'st={}'.format(token)
        }


    def onearlier(self):
        return OnearlierResponse(
            self.session.get(
                '{}/cms/routes/schedule?include=default'.format(ROOT_URL)
            ).json()
        )
        
    def onnow(self):
        return OnnowResponse(
            self.session.get(
                '{}/cms/routes/schedule?include=default'.format(ROOT_URL)
            ).json()
        )

    def onlater(self):
        return OnlaterResponse(
            self.session.get(
                '{}/cms/routes/schedule?include=default'.format(ROOT_URL)
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


"""
    OnearlierResponse sends back a list of videos that have a start time before now and
    an end time before now
"""    
class OnearlierResponse(object):
    def __init__(self, data):
        self._data = data

    def videos(self, onlyAvailable=True):

        def filterMethod(o):

            if o.get('type') != 'video':
                return False
            if not onlyAvailable:
                return True

            attributes = o.get('attributes', {})
            if len(attributes) > 0:
                av_start = parse_date(attributes['scheduleStart'])
                av_end = parse_date(attributes['scheduleEnd'])
                now = datetime.datetime.now(tz.tzutc())
                return av_start <= now > av_end

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
    OnnowResponse sends back a list of videos that have a start time before now and
    and end time after now
"""    
class OnnowResponse(object):
    def __init__(self, data):
        self._data = data

    def videos(self, onlyAvailable=True):

        def filterMethod(o):

            if o.get('type') != 'video':
                return False
            if not onlyAvailable:
                return True

            attributes = o.get('attributes', {})
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
    OnlaterResponse sends back a list of videos that have a start time later than now
"""
class OnlaterResponse(object):
    def __init__(self, data):
        self._data = data

    def videos(self, onlyAvailable=True):

        def filterMethod(o):

            if o.get('type') != 'video':
                return False
            if not onlyAvailable:
                return True

            attributes = o.get('attributes', {})
            if len(attributes) > 0:
                av_start = parse_date(attributes['scheduleStart'])
                now = datetime.datetime.now(tz.tzutc())
                return av_start >= now

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
