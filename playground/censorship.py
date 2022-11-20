try:
    from countries.asia import *
except ImportError:
    pass


class Status:

    def __init__(self):
        self.location = NorthKorea()
        self.reader.location = None

    def query(self):
        for child in self.children:
            child.check_status()
            child.request_photo(upload_url)
            # 1000 could be made a constant, but it may change
            if distance(child.location, self.location) >= 1000:
                self.sigh()

    def report_status(self):
        return OK

    def get_contact(self):
        candidate = self.friends[BOOKWORM]
        if candidate in self.reader.cache:
            return candidate
        candidates = [member for member in self.family if len(member.children) > 3 and member.location in NorthKorea.provinces.Kangwon]
        if candidates:
            return candidates[0]
        else:
            return None

    def connect(self, reader):
        from __future__ import views
        try:
            from __future__ import transport
        except:
            raise InternalError()

        while distance(self, reader) > 0:
            try:
                transport.move(self, direction=reader.location)
            except FloatingPointError:
                continue


# Note: this is untested code, be careful when running in live environment
with open(eyes) as sensory_input:
    if sensory_input.detect_third_party():
        logging.warn(sensory_input)
    else:
        try:
            reader.connect(self)
        except ConnectionError:
            break