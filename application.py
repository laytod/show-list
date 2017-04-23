import string
from models import EventList
from views import EventView, VenueView

from flask import Flask, render_template, Blueprint
app = Flask(__name__)
app.event_list = EventList()

bp = Blueprint(
    'showlist',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@bp.route('/')
def index():
    events = app.event_list.get_events()
    event_views = [EventView(e).json for e in events]
    return render_template('eventlist.html', items=event_views)


@bp.route('/venues/<int:venue_id>')
def venues(venue_id=None):
    events = app.event_list.get_events('venue_id', venue_id)
    event_views = [EventView(e).json for e in events]
    return render_template('eventlist.html', items=event_views)


@bp.route('/venue_list/', defaults={'letter': None})
@bp.route('/venue_list/<string:letter>')
def venue_list(letter=None):
    venues = app.event_list.get_venues(letter)
    venue_views = [VenueView(v).json for v in venues]
    sorted_venues = sorted(venue_views, key=lambda k: k['name'])

    # TODO: Add support for venues beginning with numbers
    return render_template(
        'venuelist.html',
        items=sorted_venues,
        letters=string.letters[:26],
    )


app.register_blueprint(bp, url_prefix='/showlist')


if __name__ == '__main__':
    app.run(debug=True)
