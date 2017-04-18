import string
from models import EventList
from views import EventView, VenueView

from flask import Flask, render_template
app = Flask(__name__)
app.event_list = EventList()


@app.route('/')
def index():
    events = app.event_list.get_events()
    event_views = [EventView(e).json for e in events]
    return render_template('eventlist.html', items=event_views)


@app.route('/venues/<venue_id>')
def venues(venue_id=None):
    events = app.event_list.get_events('venue_id', venue_id)
    event_views = [EventView(e).json for e in events]
    return render_template('eventlist.html', items=event_views)


@app.route('/venue_list/', defaults={'letter': None})
@app.route('/venue_list/<letter>')
def venue_list(letter=None):
    venues = app.event_list.get_venues(letter)
    venue_views = [VenueView(v).json for v in venues]
    sorted_venues = sorted(venue_views, key=lambda k: k['name'])
    return render_template(
        'venuelist.html',
        items=sorted_venues,
        letters=string.letters[:26],
    )


if __name__ == '__main__':
    app.run(debug=True)
