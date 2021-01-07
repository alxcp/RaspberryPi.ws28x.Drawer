import board
import neopixel
import time
import colorsys
import random
import os,sys
import effects.registry
import adafruit_neopixel_drawer

import effects.different
import effects.matrix
import effects.watch
import effects.fire
import effects.meteor_rain

from helpers import ColorRGB
from helpers import DrawerBase
from helpers import Timeout
from effects.registry import PixelEffectsRegistry
from datetime import timedelta
from adafruit_neopixel_drawer import NeoPixelDrawer

drawer = NeoPixelDrawer(300)
drawer.clear()

c1 = ColorRGB(240, 115, 239)
c2 = ColorRGB(0, 248, 0)
c3 = c1.convert(c2, 0.06700000000000005)
print(c3.to_string())

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
#pixelsEffects.runWithDrawer(drawer, waves)
pixelEffects = PixelEffectsRegistry(drawer)
#pixelEffects.next_effect()
#pixelEffects.play_effect(drawer, effects.DropsEffect())
#pixelEffects.play_effect(drawer, effects.MeteorRain(ColorRGB(255,255,255), 10, 64, True, 30))
#pixelEffects.play_effect(drawer, effect_watch.WatchEffect(32, 8, 0.1))
#pixelEffects.play_effect(drawer, meteor_rain_effect.MeteorRainEffect(drawer))
pixelEffects.play_effect(effects.effects_fire.FireEffect(drawer, 32, 8, 0))
pixelEffects.demo()
