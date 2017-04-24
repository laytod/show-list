#!./venv/bin/python
from models import EventList

import sys
import json

if __name__ == '__main__':
    event_list = EventList()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            data = f.read()

        try:
            json_data = json.loads(data)
            event_list.update_events(json_data['Events'])
        except (ValueError, TypeError):
            print "{} does not contain valid json data"
    else:
        event_list.update_events()
