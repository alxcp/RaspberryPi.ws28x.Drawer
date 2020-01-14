import time
import colorsys
import random
from colr import color
import effects
import effects_experimental
import helpers
from helpers import ColorRGB
from helpers import DrawerBase


class ConsoleDrawer(DrawerBase):
    calibration_table = [
         0,    4,   8,  12,  16,  20,  24,  28,
        32,   36,  40,  43,  46,  49,  52,  55,
        57,   59,  61,  63,  65,  67,  69,  71,
        73,   75,  78,  79,  81,  82,  84,  85,
        87,   88,  90,  91,  93,  94,  96,  97,
        99,  100, 100, 100, 100, 100, 100, 100,
        100, 100, 100, 101, 101, 101, 101, 101,
        101, 101, 101, 101, 101, 102, 102, 102,
        102, 102, 102, 102, 102, 102, 102, 102,
        102, 102, 102, 102, 102, 102, 102, 102,
        102, 102, 103, 104, 104, 104, 104, 104,
        104, 104, 105, 105, 105, 105, 105, 105,
        105, 105, 105, 105, 105, 105, 105, 105,
        105, 105, 106, 107, 108, 109, 110, 111,
        112, 113, 114, 115, 116, 117, 118, 119,
        120, 121, 122, 123, 124, 125, 126, 127,
        128, 129, 130, 131, 132, 133, 134, 135,
        136, 137, 138, 139, 140, 141, 142, 143,
        144, 145, 146, 147, 148, 149, 150, 151,
        152, 153, 154, 155, 156, 157, 158, 159,
        160, 161, 162, 163, 164, 165, 166, 167,
        168, 169, 170, 171, 172, 173, 174, 175,
        176, 177, 178, 179, 180, 181, 182, 183,
        184, 185, 186, 187, 188, 189, 190, 191,
        192, 193, 194, 195, 196, 197, 198, 199,
        200, 201, 202, 203, 204, 205, 206, 207,
        208, 209, 210, 211, 212, 213, 214, 215,
        216, 217, 218, 219, 220, 221, 222, 223,
        224, 225, 226, 227, 228, 229, 230, 231,
        232, 233, 234, 235, 236, 237, 238, 239,
        240, 241, 242, 243, 244, 245, 246, 247,
        248, 249, 250, 251, 252, 253, 254, 255
    ]

    calibrate = True
    intensity_min = 170
    intensity_max = 255

    def __init__(self, nLED):
        self.pixels = [None] * (nLED - 1)
        self.pixels_indexes = range(0, nLED - 1)
        self.nLED = nLED

    def set_color(self, position, color, calibrate=None):
        if calibrate is None:
            calibrate = self.calibrate

        if calibrate:
            self.pixels[position] = self.calibrate_color(color)
        else:
            self.pixels[position] = color

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
        self.pixels[position] = None

    def show(self):
        row = ""
        for position in self.pixels_indexes:
            pixel = self.pixels[position]

            if pixel is None:
                row += color("▌", fore=(0, 0, 0))
            else:
                row += color("▌", fore=(pixel.r, pixel.g, pixel.b))

        print(f'\r{row}', end='\r')

    def clear(self):
        for position in self.pixels_indexes:
            self.set_empty(position)

    def calibrate_color(self, color):
        return ColorRGB(
            self.calibration_table[color.r], 
            self.calibration_table[color.g], 
            self.calibration_table[color.b])


drawer = ConsoleDrawer(150)

#e = effects.RainbowWavesEffect(50, 6000)
effectsRegistry = effects.PixelEffectsRegistry()
#effectsRegistry.demo(drawer)
effectsRegistry.play_effect(drawer, effects.RandomReplacementEffect())
#effectsRegistry.play_randomized_effect(drawer)
