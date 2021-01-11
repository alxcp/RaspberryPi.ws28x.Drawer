import effects.meteor_rain

from sources.effects.registry import PixelEffectsRegistry
# from drawers.adafruit_neopixel_drawer import NeoPixelDrawer
from sources.drawers.console_drawer import ConsoleDrawer

# drawer = NeoPixelDrawer(300)
drawer = ConsoleDrawer(100)
drawer.clear()

pixelEffects = PixelEffectsRegistry(drawer)
pixelEffects.play_effect(effects.meteor_rain.MeteorRainEffect(drawer))
# pixelEffects.demo()
