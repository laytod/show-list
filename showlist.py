import jinja2
import string

from datetime import datetime
from eventlist import EventList


class ShowList(object):
    def __init__(self):
        templateLoader = jinja2.FileSystemLoader(searchpath="/home/laytod/scripts/test/templates/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        self.template = templateEnv.get_template('eventsview.html')
        self.venues_template = templateEnv.get_template('venuesview.html')

        self.event_list_object = EventList()

    def get_all_events(self):
        events = self.event_list_object.get_events()
        processed_events = [self._process_event(e) for e in events]
        return self.render(processed_events)

    def get_events_by_venue_id(self, venue_id):
        events = self.event_list_object.get_events('venue_id', venue_id)
        processed_events = [self._process_event(e) for e in events]
        return self.render(processed_events)

    def get_venues(self, letter=None):
        venues = self.event_list_object.get_venues(letter)
        processed_venues = [self._process_venue(v['Venue']) for v in venues]
        processed_venues = sorted(processed_venues, key=lambda k: k['name'])
        return self.render_venues(processed_venues)

    def _process_event(self, event_dict):
        date = datetime.strptime(event_dict['Date'], "%Y-%m-%dT%H:%M:%S")

        artists = []
        for artist_dict in event_dict['Artists']:
            artists.append({
                'name': artist_dict['Name'],
                'id': artist_dict['Id'],
            })

        return {
            'artists': artists,
            'date': date.strftime('%A, %b %d, %Y %I:%M %p'),
            'id': event_dict['Id'],
            'ticket_url': event_dict['TicketUrl'],
            'venue': self._process_venue(event_dict['Venue'])
        }

    def _process_venue(self, venue_dict):
        return {
                'address': venue_dict.get('Address'),
                'city': venue_dict.get('City'),
                'country': venue_dict.get('Country'),
                'country_code': venue_dict.get('CountryCode'),
                'id': venue_dict.get('Id'),
                'latitude': venue_dict.get('Latitude'),
                'longitude': venue_dict.get('Longitude'),
                'name': venue_dict.get('Name'),
                'state': venue_dict.get('State'),
                'state_code': venue_dict.get('StateCode'),
                'url': venue_dict.get('Url'),
                'zipcode': venue_dict.get('ZipCode'),

            }

    def render_venues(self, venues):
        return self.venues_template.render({
            'venues': venues,
            'letters': string.letters[:26]
        })

    def render(self, events):
        return self.template.render({
            'events': events,
        })


if __name__ == '__main__':
    sl = ShowList()
    show_list_html = sl.get_events_by_venue_id(8318)

    print show_list_html

