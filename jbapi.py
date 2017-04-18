import json
import requests

from decorators import throttle
from page import Page


class JBapiError(Exception):
    pass


class JBapi(object):
    def __init__(self, api_key=None, zipcode=33584, radius=50):
        self.config = self._read_config()

        self.api_key = api_key or self.default_api_key
        self.zipcode = zipcode
        self.radius = radius

    def _read_config(self, path=None):
        path = path or 'config.json'

        # TODO: Add more error handling for config reading
        with open(path, 'r') as config:
            config_data = config.read()

        try:
            return json.loads(config_data)
        except (ValueError, TypeError):
            raise JBapiError('Cannot parse config')

    @property
    def default_api_key(self):
        api_key = self.config.get('api_key')
        assert api_key is not None, 'No api_key in config.json'
        return api_key

    @property
    def url(self):
        api_url = 'http://api.jambase.com/events' + \
            '?zipCode={zipcode}&radius={radius}&api_key={api_key}'
        return api_url.format(
            zipcode=self.zipcode,
            radius=self.radius,
            api_key=self.api_key,
        )

    @throttle(seconds=1)
    def get_page(self, page_number):
        """ Throttle the api call to 1 per second max
        """
        request_url = self.url + '&page={page}'.format(page=page_number)
        response = requests.get(request_url)

        if response.status_code == 200:
            return response.json()
        else:
            # TODO: Add more error handling for more specific HTTP codes
            raise JBapiError('API Request Failed: {code} {msg}'.format(
                code=response.status_code,
                msg=response.reason
            ))

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
