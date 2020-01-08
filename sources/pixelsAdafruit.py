import board
import neopixel
import time
import colorsys
import random
import os,sys
import pixelsEffects
from pixelsEffects import *

class NeoPixelDrawer(object):
    def __init__(self, nLED):
        self.pixels = neopixel.NeoPixel(board.D18,nLED,auto_write=False)
        self.nLED = nLED
        self.Clear()

    def SetColor(self, position, color):
        self.pixels[position] = (color.R, color.G, color.B)

    def Show(self):
        self.pixels.show()

    def Clear(self):
        self.pixels.fill((0,0,0))
        self.pixels.show()

    def GetCopy(self):
        result = []
        for pixel in self.pixels:
            result.append(pixelsEffects.ColorRGB(pixel[0], pixel[1], pixel[2]))
        return result

drawer = NeoPixelDrawer(300)

#rainbow_hsv(200)
#e = rainbow_hsv
#e = pixelsEffects.rainbow_hsv2
#e = stripes
#e = rings
#e = boom
#e = pixelsEffects.fullFade
#e = pixelsEffects.randomReplacement
#e = pixelsEffects.switchColors
#run_effect(e,300,8)
pixelsEffects.intensity = 50
pixelsEffects.runWithDrawer(drawer, waves)
#pixelsEffects.runRandomized(drawer)

