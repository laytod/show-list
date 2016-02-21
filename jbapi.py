import requests
from decorators import throttle
from page import Page
from datetime import datetime

api_key = 'acd6pyauxav8smmkqndgcbaq'


class JBapi(object):
    def __init__(self, api_key, zipcode=33584, radius=50):
        self.api_key = api_key
        self.zipcode = zipcode
        self.radius = radius

    @property
    def url(self):
        return 'http://api.jambase.com/events?zipCode={zipcode}&radius={radius}&api_key={api_key}'.format(
            zipcode=self.zipcode,
            radius=self.radius,
            api_key=self.api_key,
        )

    @throttle(seconds=1)
    def get_page(self, page_number):
        """ Throttle the api call to 1 per second max
        """
        print '-- ' + str(datetime.now())
        request_url = self.url + '&page={page}'.format(page=page_number)
        print request_url
        response = requests.get(request_url)
        return response.json()

    def get_events(self):
        """ Get all events within a range of a zipcode
        """
        page = Page(self.get_page(0))
        all_events = page.event_data

        while len(all_events) < page.info.total_results:
            next_page_number = page.info.page_number + 1

            page_result = None
            while page_result is None:
                page_result = self.get_page(next_page_number)

            page = Page(page_result)
            all_events += page.event_data

        return all_events
