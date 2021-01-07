import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math

from effects.base import PixelEffect

from helpers.color_rgb import ColorRGB

class MeteorRainEffect(PixelEffect):
    def __init__(self, drawer, frame_delay = 0):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.meteors = []
        self.meteors.append(Meteor())        
        
    def play_frame(self):
        if (random.random() > 0.995 and len(self.meteors) < 5):
            self.meteors.append(Meteor())
        
        self.drawer.clear(False)
        to_remove = []
        
        for meteor in self.meteors:
            meteor.altitude = meteor.altitude + meteor.speed
            self.draw_meteor(meteor)
            self.draw_tail(meteor)
            if meteor.altitude >= self.drawer.nLED and len(meteor.tail_pixels) == 0:
                to_remove.append(meteor)
        
        for meteor in to_remove:
            self.meteors.remove(meteor)
            
        self.drawer.show()
    
    def draw_meteor(self, meteor):
        for delta in range(1, meteor.radius - 1):
            c = meteor.color.multiply(1 / delta)
            
            pixel = meteor.altitude - delta - 1
            if pixel > 0 and pixel < self.drawer.nLED:
                self.drawer.set_color(pixel, c)
            
            pixel = meteor.altitude + delta + 1
            if pixel < self.drawer.nLED:
                self.drawer.set_color(pixel, c)
                
        if meteor.altitude < self.drawer.nLED:
            self.drawer.set_color(meteor.altitude, meteor.color)
    
    def draw_tail(self, meteor):
        if meteor.altitude - meteor.radius - 1 < 0:
            return
        
        if meteor.altitude - meteor.radius - 1 < self.drawer.nLED:
            meteor.tail_pixels.append(TailPixel(meteor.altitude - meteor.radius - 1, meteor.color))
        
        to_remove = []
        
        for tail_pixel in meteor.tail_pixels:
            tail_pixel.heat = tail_pixel.heat - tail_pixel.speed
            if tail_pixel.heat < 0:
                to_remove.append(tail_pixel)
            else:
                self.drawer.set_color(tail_pixel.position, tail_pixel.color.multiply(tail_pixel.heat))
        
        for removed in to_remove:
            meteor.tail_pixels.remove(removed)                

        
class Meteor(object):
    def __init__(self):
        self.altitude = 0
        self.speed = 1
        self.color = ColorRGB.random(3, 0, 80)
        self.radius = 3
        self.tail_pixels = []
                           
class TailPixel(object):
    heat = 1
    
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.heat = 0.5
        self.speed = (random.random() + 0.05) / 15
