from datetime import datetime


class Timeout(object):
    def __init__(self, delta):
        self.EndTime = datetime.now() + delta

    def is_expired(self):
        return datetime.now() > self.EndTime


class TimeoutInfinite(Timeout):
    def __init__(self):
        super().__init__(datetime.now() - datetime.now())

    def is_expired(self):
        return False
