
class DrawerBase(object):
    calibration_table = [range(0, 255)]
    n_led = 0

    frames = []
    recording = False

    def __init__(self, n_led):
        self.n_led = n_led
        self.pixels_indexes = range(0, n_led - 1)

    def begin_record(self):
        self.recording = True

    def stop_record(self):
        self.recording = False

    def replay(self, timeout):
        raise NotImplementedError()

    def set_color(self, position, color, calibrate=None):
        raise NotImplementedError()

    def set_color_raw(self, position, r, g, b, calibrate=None):
        raise NotImplementedError()

    def set_empty(self, position):
        raise NotImplementedError()

    def show(self):
        raise NotImplementedError()

    def clear(self, show=True):
        raise NotImplementedError()

    def calibrate_color(self, color):
        raise NotImplementedError()

    def show_frame(self, frame):
        raise NotImplementedError()
