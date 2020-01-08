import time
import colorsys
import random
from colr import color
import pixelsEffects

blinks = []

class ConsoleDrawer(object):
    def __init__(self, nLED):
        self.pixels = []
        for z in range(0, nLED):
            self.pixels.append(pixelsEffects.ColorRGB())
        self.nLED = nLED

    def SetColor(self, position, color):
        self.pixels[position] = color

    def Show(self):
        row = ""        
        for position in range(0, self.nLED - 1):
            pixel = self.pixels[position]
            row += color(" ", back=(pixel.R, pixel.G, pixel.B))
        print('\r'+row, end='\r')

    def Clear(self):
        for position in range(0,self.nLED-1):
            self.SetColor(position, pixelsEffects.ColorRGB(0,0,0))

    def GetCopy(self):
        result = []
        for pixel in self.pixels:
            result.append(pixel)
        return result

drawer = ConsoleDrawer(100)

#rainbow_hsv(200)
#e = rainbow_hsv
#e = pixelsEffects.rainbow_hsv2
#e = pixelsEffects.beads
#e = pixelsEffects.randomBlinks
#e = pixelsEffects.color_bounce
#e = pixelsEffects.rule30
#e = stripes
#e = rings
#e = boom
#run_effect(e,300,8)
pixelsEffects.intensity = 200
#pixelsEffects.runWithDrawer(drawer, e)
pixelsEffects.runRandomized(drawer)
