import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
import helpers

import effects.different
import effects.matrix
import effects.watch
import effects.fire
import effects.meteor_rain

import sys, traceback
from helpers.timeouts import Timeout
from helpers.timeouts import TimeoutInfinite
#from helpers.color_rgb import ColorRGB

class PixelEffectsRegistry(object):
    effects = []
    current_effect_number = 0

    def __init__(self, drawer):
        self.drawer = drawer
        self.register(effects.different.RainbowHSVEffect(drawer))
        self.register(effects.different.RainbowHSV2Effect(drawer))
        self.register(effects.different.BeadsEffect(drawer))
        self.register(effects.different.RandomBlinksEffect(drawer))
        #self.register(effects.FullFadeEffect(drawer))
        self.register(effects.different.WavesEffect(drawer, 400, 4000))
        self.register(effects.different.RainbowWavesEffect(drawer, 400, 4000))
        self.register(effects.different.DropsEffect(drawer))
        self.register(effects.meteor_rain.MeteorRainEffect(drawer))
        self.register(effects.fire.FireEffect(drawer, 32, 8, 0))        

    def register(self, effect):
        self.effects.append(effect)

    def play_effect(self, effect, timeout = None):
        if timeout is None:
            timeout = TimeoutInfinite()

        try:
            effect.play(timeout)
        except KeyboardInterrupt:
            self.drawer.clear()
            
    def next_effect(self):
        self.current_effect_number = self.current_effect_number+1
        if self.current_effect_number > len(self.effects)-1:
            self.current_effect_number = 0
        
        next_effect = self.effects[self.current_effect_number]

        try:
            self.play_effect(next_effect)
        except KeyboardInterrupt:
            self.drawer.clear()
            return
        except:
            traceback.print_exc()

    def play_randomized_effect(self):
        while True:
            next_effect_index = random.randint(0, len(self.effects) - 1)
            next_effect = self.effects[next_effect_index]

            timeout = timedelta(seconds = random.randint(10, 10))

            print (f"\r\nWill run {next_effect} for a {timeout}")

            try:
                self.play_effect(next_effect, Timeout(timeout))
            except KeyboardInterrupt:
                self.drawer.clear()
                return
            except:
                traceback.print_exc()

    def demo(self):
        next_effect_index = -1

        while True:
            next_effect_index += 1
            if next_effect_index >= len(self.effects):
                next_effect_index = 0

            next_effect = self.effects[next_effect_index]

            timeout = timedelta(seconds = 10)

            print (f"\r\nWill run {next_effect} for a {timeout}")

            try:
                self.play_effect(next_effect, Timeout(timeout))
            except KeyboardInterrupt:
                self.drawer.clear()
                return
            except Exception as e:
                print(e)