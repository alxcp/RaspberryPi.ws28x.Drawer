import time
from colr import color
from sources.helpers.color_rgb import ColorRGB
from sources.drawers.base import DrawerBase


class ConsoleDrawer(DrawerBase):
    calibration_table = None

    calibrate = False
    intensity_min = 170
    intensity_max = 255

    def __init__(self, n_led):
        super().__init__(n_led)
        self.pixels = [ColorRGB(0, 0, 0)] * n_led
        self.pixels_indexes = range(0, n_led)

    def set_color(self, position, target_color, calibrate=None):
        if calibrate is None:
            calibrate = self.calibrate

        if calibrate:
            self.pixels[position] = self.calibrate_color(target_color)
        else:
            self.pixels[position] = target_color

    def set_color_raw(self, position, r, g, b, calibrate=None):
        if calibrate is None:
            calibrate = self.calibrate

        if calibrate:
            self.pixels[position] = ColorRGB(
                self.calibration_table[int(r)],
                self.calibration_table[int(g)],
                self.calibration_table[int(b)])
        else:
            self.pixels[position] = ColorRGB(int(r), int(g), int(b))

    def set_empty(self, position):
        self.pixels[position] = ColorRGB()

    def show(self):
        row = ""
        for position in self.pixels_indexes:
            pixel = self.pixels[position]

            if pixel is None:
                row += color('█', fore=(0, 0, 0))
            else:
                row += color('█', fore=(pixel.r, pixel.g, pixel.b))

        time.sleep(0.05)

        print(f'\r{row}', end='\r')

        if self.recording:
            self.frames.append(self.pixels.copy())

    def clear(self, show=True):
        for position in self.pixels_indexes:
            self.set_empty(position)

    def calibrate_color(self, original_color):
        return ColorRGB(
            self.calibration_table[original_color.r],
            self.calibration_table[original_color.g],
            self.calibration_table[original_color.b])

    def show_frame(self, frame):
        self.pixels = frame
        self.show()

    def replay(self, timeout):
        while not timeout.is_expired():
            for frame in self.frames:
                self.show_frame(frame)
