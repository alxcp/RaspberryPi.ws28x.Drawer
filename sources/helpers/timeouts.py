from datetime import datetime


class Timeout(object):
    def __init__(self, delta):
        self.EndTime = datetime.now() + delta
        self.delta = delta

    def is_expired(self):
        return datetime.now() > self.EndTime

    def get_display_name(self):
        return "{0} (Until {1}".format(self.delta, self.EndTime)


class TimeoutInfinite(Timeout):
    def __init__(self):
        super().__init__(datetime.now() - datetime.now())

    def is_expired(self):
        return False

    def get_display_name(self):
        return "Infinite"
