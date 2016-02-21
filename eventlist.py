import pymongo

from jbapi import JBapi, api_key


class EventList(object):
    def __init__(self):
        self.jambase_api = JBapi(api_key)
        conn = pymongo.MongoClient()
        self.db = conn.jambase

    def update_events(self):
        event_data = self.jambase_api.get_events()
        self.db.drop_collection('events')
        self.db.events.insert(event_data)

    def get_events(self, search_filter=None, search_value=None):
        events = self.db.events

        if search_filter == 'venue_id':
            x = [e for e in events.find(
                {'Venue.Id': int(search_value)}
            )]

            return x

        return [e for e in events.find()]

    def get_venues(self, letter=None):
        events = self.db.events
        venue_names = events.find().distinct('Venue.Name')

        if letter:
            venue_names = [n for n in venue_names if letter.lower() == n[0].lower()]

        venues = []
        for name in venue_names:
            venue = events.find_one({'Venue.Name': name})
            venues.append(venue)

        return venues


if __name__ == '__main__':
    el = EventList()

    events = el.get_events()

    for i in events:
        print i
        print '--'

    print len(events)
