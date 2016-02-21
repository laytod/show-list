from datetime import datetime


class Event(object):
    def __init__(self, event_dict):
        self.artists = [Artist(a) for a in event_dict['Artists']]
        self.date = datetime.strptime(event_dict['Date'], "%Y-%m-%dT%H:%M:%S")
        self.venue = Venue(event_dict['Venue'])


class Venue(object):
    def __init__(self, venue_dict):
        self.name = venue_dict['Name']
        self.address = venue_dict['Address']
        self.city = venue_dict['City']
        self.state = venue_dict['State']
        self.zipcode = venue_dict['ZipCode']
        self.url = venue_dict['Url']


class Artist(object):
    def __init__(self, artist_dict):
        self.name = artist_dict['Name']
        self.id = artist_dict['Id']
