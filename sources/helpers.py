import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
from colr import color


class PixelEffect(object):
    def play(self, drawer, timeout):
        raise NotImplementedError()

class DrawerBase(object):
    calibration_table = [range(0, 255)]
    nLED = 0

    frames = []
    recording = False

    def __init__(self, nLED):
        self.nLED = nLED
        self.pixels_indexes = range(0, nLED - 1)

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

    def clear(self):
        raise NotImplementedError()

    def calibrate_color(self, color):
        raise NotImplementedError()

    def show_frame(self, frame):
        raise NotImplementedError()


class ColorRGB(object):
    r = 0
    g = 0
    b = 0

    def __init__(self, r = 0, g = 0, b = 0):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def multiply(self, k, preserve_components=False):
        r = min(int(self.r * k), 255)
        g = min(int(self.g * k), 255)
        b = min(int(self.b * k), 255)

        if preserve_components:
            if self.r > 0 and r == 0:
                r = 1
            if self.g > 0 and g == 0:
                g = 1
            if self.b > 0 and b == 0:
                b = 1

        return ColorRGB(r, g, b)

    def set_component(self, channel_number, value, drawer=None):
        if channel_number == 0:
            self.r = value
        elif channel_number == 1:
            self.g = value
        elif channel_number == 2:
            self.b = value

    def to_string(self):
        return f"({self.r}, {self.g}, {self.b})"

    @staticmethod
    def random(channels_max=3, intensity_min=0, intensity_max=255):
        result = ColorRGB()
        if channels_max == 1:
            result.set_component(
                random.randint(0, 2), 
                random.randint(intensity_min, intensity_max))
        elif channels_max == 2:
            result.set_component(
                random.randint(0, 2), 
                random.randint(intensity_min, intensity_max))
            result.set_component(
                random.randint(0, 2), 
                random.randint(intensity_min, intensity_max))
        elif channels_max == 3:
            result.set_component(
                random.randint(0, 2), 
                random.randint(intensity_min, intensity_max))
            result.set_component(
                random.randint(0, 2), 
                random.randint(intensity_min, intensity_max))
            result.set_component(
                random.randint(0, 2), 
                random.randint(intensity_min, intensity_max))
        return result

    @staticmethod
    def CHSV(nLED, position, saturation, times_per_stripe = 1.0):
        p = 1.0 / nLED / times_per_stripe
        pixel = colorsys.hsv_to_rgb(position * p, 1, 1)
        return ColorRGB(
            pixel[0] * saturation, 
            pixel[1] * saturation, 
            pixel[2] * saturation)


class Timeout(object):
    def __init__(self, delta):
        self.EndTime = datetime.now() + delta

    def is_expired(self):
        return datetime.now() > self.EndTime


class TimeoutInfinite(object):
    def is_expired(self):
        return False