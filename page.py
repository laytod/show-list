from event import Event


class Page(object):
    def __init__(self, page_dict):
        self.info = Info(page_dict['Info'])
        self.events = EventList(page_dict['Events'])
        self.event_data = page_dict['Events']

    def to_json(self):
        return {
            'info': self.info.to_json(),
            'events': self.event_data is not None,
        }


class Info(object):
    def __init__(self, info_dict):
        self.page_number = info_dict['PageNumber']
        self.message = info_dict['Message']
        self.total_results = info_dict['TotalResults']

    def to_json(self):
        return {
            'page_number': self.page_number,
            'message': self.message,
            'total_results': self.total_results,
        }


class EventList(object):
    def __init__(self, events_dict):
        self._data = events_dict
        self.items = []

        for event_dict in self._data:
            event_object = Event(event_dict)
            self.items.append(event_object)

    def sort_by(self):
        pass
