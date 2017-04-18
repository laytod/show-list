

class Page(object):
    def __init__(self, page_dict):
        self.info = Info(page_dict['Info'])
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
