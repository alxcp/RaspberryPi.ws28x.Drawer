import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
import helpers
from helpers import *

class SkittlesEffect(PixelEffect):
    def play(self, drawer, timeout):    
        while not timeout.is_expired():
            for z in drawer.pixels_indexes:
                drawer.set_color(z, ColorRGB.random(2, 3, 20))
            drawer.show()
            time.sleep(3)

class ColorRunawayEffect(PixelEffect):
    def play(self, drawer, timeout):    
        while not timeout.is_expired():
            ps = random.randint(0, drawer.n_led - 1)
            pl = pr = ps
            color = ColorRGB.random(2, drawer.intensity_min, drawer.intensity_max)
            speed = 0
            drawer.set_color(ps, color)
            drawer.show()
            while True:
                speed += 1
                pl -= speed
                pr += speed

                if pl < 0 or pr > drawer.n_led - 1:
                    break

                for p in range(pl,pr):
                    drawer.set_color(p,color)
                
                drawer.show()
                time.sleep(0.1)                

class SwitchColorsEffect(PixelEffect):
    def play(self, drawer, timeout):
        first_color = ColorRGB(255, 153, 51).multiply(0.1)
        second_color = ColorRGB(102, 153, 255).multiply(0.1)
        step = 0

        while not timeout.is_expired():
            if step == 1:
                step = 2
            else:
                step = 1

            for ln in range(0,drawer.n_led - 1, 3):
                if step == 1:
                    drawer.set_color(ln, first_color)
                    drawer.set_color(ln+1, second_color)
                    drawer.set_color(ln+2, second_color)
                else:
                    drawer.set_color(ln, second_color)
                    drawer.set_color(ln+1, first_color)
                    drawer.set_color(ln+2, first_color)
            drawer.show()
            time.sleep(1)