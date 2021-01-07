import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math

from effects.base import MatrixPixelEffect

from helpers.color_rgb import ColorRGB

class WatchEffect(MatrixPixelEffect):
    def __init__(self, width, height, frame_delay = 0.3):
        MatrixPixelEffect.__init__(self, width, height, 1, frame_delay)
        self.base_color = ColorRGB.random()
        self.new_base_color = ColorRGB.random()
        self.color = self.base_color
        self.color_conversion_progress = 0
        self.last_time = ''
        self.sprites = []
        self.sprites.append([
            [1,1,1],
            [1,0,1],
            [1,0,1],
            [1,0,1],
            [1,0,1],
            [1,0,1],
            [1,1,1]])
        self.sprites.append([
            [0,0,1],
            [0,0,1],
            [0,0,1],
            [0,0,1],
            [0,0,1],
            [0,0,1],
            [0,0,1]])
        self.sprites.append([
            [1,1,1],
            [0,0,1],
            [0,0,1],
            [1,1,1],
            [1,0,0],
            [1,0,0],
            [1,1,1]])
        self.sprites.append([
            [1,1,1],
            [0,0,1],
            [0,0,1],
            [1,1,1],
            [0,0,1],
            [0,0,1],
            [1,1,1]])
        self.sprites.append([
            [1,0,1],
            [1,0,1],
            [1,0,1],
            [1,1,1],
            [0,0,1],
            [0,0,1],
            [0,0,1]])        
        self.sprites.append([
            [1,1,1],
            [1,0,0],
            [1,0,0],
            [1,1,1],
            [0,0,1],
            [0,0,1],
            [1,1,1]])
        self.sprites.append([
            [1,1,1],
            [1,0,0],
            [1,0,0],
            [1,1,1],
            [1,0,1],
            [1,0,1],
            [1,1,1]])
        self.sprites.append([
            [1,1,1],
            [0,0,1],
            [0,0,1],
            [0,1,0],
            [0,1,0],
            [1,0,0],
            [1,0,0]])
        self.sprites.append([
            [1,1,1],
            [1,0,1],
            [1,0,1],
            [1,1,1],
            [1,0,1],
            [1,0,1],
            [1,1,1]])
        self.sprites.append([
            [1,1,1],
            [1,0,1],
            [1,0,1],
            [1,1,1],
            [0,0,1],
            [0,0,1],
            [1,1,1]])
        self.sprites.append([
            [0,0,0],
            [0,0,0],
            [0,1,0],
            [0,0,0],
            [0,1,0],
            [0,0,0],
            [0,0,0]])
        
    def play_frame(self, drawer):
        t = datetime.now().strftime("%H:%M:%S")
        if self.last_time == t:
            return
        
        self.last_time = t
        
        self.color_conversion_progress = self.color_conversion_progress + 0.01
        
        if self.color_conversion_progress > 1:
            self.base_color = self.new_base_color
            self.new_base_color = ColorRGB.random()
            self.color_conversion_progress = 0
            
        self.color = self.base_color.convert(self.new_base_color, self.color_conversion_progress)

        
        sec = datetime.now().second
        i = 0
        drawer.clear(False)
        print(t)
        
        for s in t:
            if s == ':':
                if sec % 2 == 0:
                    self.print_symbol(drawer, 10, i)
            else:
                self.print_symbol(drawer, int(s), i)
            i = i + 1
        
        drawer.show()
        
    def print_symbol(self, drawer, symbol_index, position):
        x = 4 * position
        sprite = self.sprites[symbol_index]
        for sx in range(3):
            for sy in range(7):
                pixel = super(WatchEffect, self).translateToMatrixColumns(x + sx + 2,sy + 1)
                if sprite[sy][sx] == 1:
                    drawer.set_color(pixel, self.color)