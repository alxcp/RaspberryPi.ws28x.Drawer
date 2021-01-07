


class Timeout(object):
    def __init__(self, delta):
        self.EndTime = datetime.now() + delta

    def is_expired(self):
        return datetime.now() > self.EndTime


class TimeoutInfinite(object):
    def is_expired(self):
        return False