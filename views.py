from datetime import datetime


class EventView(object):
    def __init__(self, data):
        self._data = data

        self.id = self._data.get('Id')
        self.ticket_url = self._data.get('TicketUrl')
        self.venue = VenueView(self._data['Venue']).json

    @property
    def artists(self):
        artists = []
        for artist in self._data.get('Artists', []):
            artists.append({
                'name': artist.get('Name'),
                'id': artist.get('Id'),
            })

        return artists

    @property
    def date(self):
        date = datetime.strptime(self._data.get('Date'), "%Y-%m-%dT%H:%M:%S")

        return {
            'day_of_week': date.strftime('%A'),
            'date': date.strftime('%b %d, %Y'),
            'time': date.strftime('%I:%M %p'),
        }

    @property
    def json(self):
        json_dict = self.__dict__
        json_dict.update({
            'artists': self.artists,
            'date': self.date,
        })
        return json_dict


class VenueView(object):
    def __init__(self, data):
        self._data = data

        self.address = self._data.get('Address')
        self.city = self._data.get('City')
        self.country = self._data.get('Country')
        self.country_code = self._data.get('CountryCode')
        self.id = self._data.get('Id')
        self.latitude = self._data.get('Latitude')
        self.longitude = self._data.get('Longitude')
        self.name = self._data.get('Name')
        self.state = self._data.get('State')
        self.state_code = self._data.get('StateCode')
        self.url = self._data.get('Url')
        self.zipcode = self._data.get('ZipCode')

    @property
    def google_map_search_term(self):
        address = self._data.get('Address').split(' ')
        address = ' '.join(address[1:])

        google_maps_search_term = '{name}, {addr}, {city}, {state}'.format(
            name=self.name,
            addr=address,
            city=self.city,
            state=self.state,
        )

        return google_maps_search_term.replace(' ', '+')

    @property
    def json(self):
        return self.__dict__
