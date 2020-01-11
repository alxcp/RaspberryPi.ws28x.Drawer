import time
import colorsys
import random
from colr import color
import effects
from effects import *
import helpers
from helpers import *

class ConsoleDrawer(DrawerBase):
    CalibrationTable = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 43, 46, 49, 52, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 78, 79, 81, 82, 84, 85, 87, 88, 90, 91, 93, 94, 96, 97, 99, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 103, 104, 104, 104, 104, 104, 104, 104, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    CorrectGammaDefault = True
    IntensityMin = 170
    IntensityMax = 255

    def __init__(self, nLED):
        self.pixels = []
        for z in range(0, nLED):
            self.pixels.append(ColorRGB())
        self.nLED = nLED

    def SetColor(self, position, color, calibrate = None):
        if calibrate is None:
            calibrate = self.CorrectGammaDefault

        if calibrate:            
            self.pixels[position] = self.CalibrateColor(color)
        else:
            self.pixels[position] = color

    def Show(self):
        row = ""        
        for position in range(0, self.nLED - 1):
            pixel = self.pixels[position]
            row += color("▌", fore=(pixel.R, pixel.G, pixel.B))
        print('\r'+row, end='\r')

    def Clear(self):
        for position in range(0,self.nLED-1):
            self.SetColor(position, ColorRGB())

    def GetCopy(self):
        result = []
        for pixel in self.pixels:
            result.append(pixel)
        return result

    def CalibrateColor(self, color):
        return super().CalibrateColor(color)

drawer = ConsoleDrawer(150)

#rainbow_hsv(200)
#e = rainbow_hsv
#e = pixelsEffects.rainbow_hsv2
#e = pixelsEffects.beads
#e = pixelsEffects.randomBlinks
#e = pixelsEffects.color_bounce
#e = pixelsEffects.rule30
#e = waves
#e = stripes
#e = rings
#e = boom
#run_effect(e,300,8)
#correctGammaDefault = False

#drawer.PlayEffect(e)
effects = PixelEffectsRegistry()
effects.PlayRandomizedEffect(drawer)


#pixelsEffects.runRandomized(drawer)
