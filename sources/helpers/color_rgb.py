import colorsys
import random


class ColorRGB(object):
    r = 0
    g = 0
    b = 0

    def __init__(self, r=0, g=0, b=0):
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

    def convert(self, target, progress):
        if progress < 0 or progress > 1:
            raise ArgumentOutOfRangeException()

        rc = self.r - int((self.r - target.r) * progress)
        gc = self.g - int((self.g - target.g) * progress)
        bc = self.b - int((self.b - target.b) * progress)

        result = ColorRGB(rc, gc, bc)

        if rc > 255 or gc > 255 or bc > 255:
            print(result.to_string())
            print(self.to_string())
            print(target.to_string())
            print(progress)

        return result

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
    def CHSV(n_led, position, saturation, times_per_stripe=1.0):
        p = 1.0 / n_led / times_per_stripe
        pixel = colorsys.hsv_to_rgb(position * p, 1, 1)
        return ColorRGB(
            pixel[0] * saturation,
            pixel[1] * saturation,
            pixel[2] * saturation)
