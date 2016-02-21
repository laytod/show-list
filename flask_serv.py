import string
from eventlist import EventList
from datetime import datetime

from flask import Flask, render_template
app = Flask(__name__)


event_list = EventList()


@app.route('/')
def index():
    events = event_list.get_events()
    processed_events = [_process_event(e) for e in events]
    return render_template('eventlist.html', items=processed_events)


@app.route('/venues/<venue_id>')
def venues(venue_id=None):
    events = event_list.get_events('venue_id', venue_id)
    processed_events = [_process_event(e) for e in events]
    return render_template('eventlist.html', items=processed_events)


@app.route('/venue_list/', defaults={'letter': None})
@app.route('/venue_list/<letter>')
def venue_list(letter=None):
    venues = event_list.get_venues(letter)
    processed_venues = [_process_venue(v['Venue']) for v in venues]
    processed_venues = sorted(processed_venues, key=lambda k: k['name'])
    return render_template(
        'venuelist.html',
        items=processed_venues,
        letters=string.letters[:26],
    )


def _process_event(event_dict):
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
        'venue': _process_venue(event_dict['Venue'])
    }


def _process_venue(venue_dict):
    address = venue_dict.get('Address').split(' ')
    address = ' '.join(address[1:])

    gmst = '{}, {}, {}, {}'.format(
        venue_dict.get('Name'),
        address,
        venue_dict.get('City'),
        venue_dict.get('State'),
    ).replace(' ', '+')
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
            'google_map_search_term': gmst,
        }

if __name__ == '__main__':
    app.run(debug=True)
