import pymongo

from jbapi import JBapi


class EventList(object):
    def __init__(self):
        self.jambase_api = JBapi()
        conn = pymongo.MongoClient()
        self.db = conn.jambase
        self.events = self.db.events

    def update_events(self, event_data=None):
        if event_data is None:
            event_data = self.jambase_api.get_events()

        self.db.drop_collection('events')
        self.db.events.insert(event_data)

    def get_events(self, search_filter=None, search_value=None):
        query = {}

        if search_filter == 'venue_id':
            query = {'Venue.Id': int(search_value)}

        return self.events.find(query)

    def get_venues(self, letter=None):
        venue_names = self.events.find().distinct('Venue.Name')

        if letter:
            # filter venue names by first letter
            letter = letter.lower()
            venue_names = filter(lambda k: k.lower().startswith(letter), venue_names)

        # TODO: Could likely use a regex here...
        return self.events.find({'Venue.Name': {'$in': venue_names}})


if __name__ == '__main__':
    import pprint
    el = EventList()

    events = el.get_events()

    for i in events:
        pprint.pprint(i)
        print '-----'

    print events.count()
