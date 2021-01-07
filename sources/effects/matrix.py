import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
from effects.base import PixelEffect
from effects.base import MatrixPixelEffect
#import helpers
#from helpers import ColorRGB
#from helpers import PixelEffect
#from helpers import MatrixPixelEffect

class Stripe(PixelEffect):
    def __init__(self, width, height, blocks):
        self.width = width
        self.height = height
        self.blocks = blocks
        self.block_length = width * height
        
        
    def play(self, drawer, timeout):
        translate = 0        
        c = ColorRGB.random()

        while not timeout.is_expired():

            if translate == (self.width) * self.blocks - 1:
                translate = 0
                c = ColorRGB.random()
            else:
                translate = translate + 1
                
            for x in range(1, self.width * self.blocks):
                for y in range(1, self.height + 1):
                    pixel = self.translateToMatrixColumns(x,y)
                    if x >= translate - 1 and x < translate + 1:
                        drawer.set_color_raw(pixel, r = c.r, g = c.g, b = c.b)
                    else:
                        drawer.set_empty(pixel)

            drawer.show()
            #time.sleep(0.03)
            
    def translateToMatrixRows(self, x, y):
        current_block = x // self.width
        block_shift = current_block * self.block_length
        
        x = x - current_block * self.width
        
        if (y % 2) == 0:
            return y * self.width - x - 1 + block_shift
        else:
            return (y - 1) * self.width + x + block_shift
        
    def translateToMatrixColumns(self, x, y):
        current_block = y // self.height
        block_shift = current_block * self.block_length
        
        y = y - current_block * self.height
        
        if (x % 2) == 0:
            return x * self.height - y - 1 + block_shift
        else:
            return (x - 1) * self.height + y + block_shift

            
class RandomFill(PixelEffect):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        
    def play(self, drawer, timeout):
        while not timeout.is_expired():
            pixel = random.randint(0, drawer.nLED - 1)
            c = ColorRGB.random()
            drawer.set_color(pixel, c)
            drawer.show()
            
    def translateToMatrix(self, x, y):
        if (y % 2) == 0:
            return (y + 1) * self.width - x - 1
        else:
            return y * self.width + x

class EachPixelEffect(MatrixPixelEffect):
    def __init__(self, width, height, frame_delay = -1):
        MatrixPixelEffect.__init__(self, width, height, frame_delay)
        
    def play_frame(self, drawer):
        c = ColorRGB.random()
        for x in range(self.width):
            for y in range(self.height):
                pixel = super(EachPixelEffect, self).translateToMatrixColumns(x,y)
                drawer.clear()
                drawer.set_color(pixel, c)
                drawer.show()
                time.sleep(0.1)
                
class EachPixelEffect1(MatrixPixelEffect):
    def __init__(self, width, height, frame_delay = 0):
        MatrixPixelEffect.__init__(self, width, height, frame_delay)
        
    def play_frame(self, drawer):
        c = ColorRGB.random()
        for pixel in range(drawer.nLED):
            drawer.clear()
            drawer.set_color(pixel, c)
            drawer.show()
            #time.sleep(0.1)
            


#class TaisaEffect(MatrixPixelEffect):
#    def __init__(self, width, height):
#        MatrixPixelEffect.__init__(self, width, height)
#        self.image = new[]
#        self.image.append([
        
    