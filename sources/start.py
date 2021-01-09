import effects.different
import effects.watch
import effects.fire
import effects.meteor_rain

from helpers.color_rgb import ColorRGB
from effects.registry import PixelEffectsRegistry
# from drawers.adafruit_neopixel_drawer import NeoPixelDrawer
from drawers.virtual_console_drawer import ConsoleDrawer

# drawer = NeoPixelDrawer(300)
drawer = ConsoleDrawer(100)
drawer.clear()

# rainbow_hsv(200)
# e = rainbow_hsv
# e = pixelsEffects.rainbow_hsv2
# e = stripes
# e = rings
# e = boom
# e = pixelsEffects.fullFade
# e = pixelsEffects.randomReplacement
# e = pixelsEffects.switchColors
# run_effect(e,300,8)
# pixelsEffects.runWithDrawer(drawer, waves)
pixelEffects = PixelEffectsRegistry(drawer)
# pixelEffects.next_effect()
# pixelEffects.play_effect(drawer, effects.DropsEffect())
# pixelEffects.play_effect(drawer, effects.MeteorRain(ColorRGB(255,255,255), 10, 64, True, 30))
# pixelEffects.play_effect(drawer, effect_watch.WatchEffect(32, 8, 0.1))
pixelEffects.play_effect(effects.meteor_rain.MeteorRainEffect(drawer))
# pixelEffects.play_effect(effects.fire.FireEffect(drawer, 32, 8, 0))
pixelEffects.demo()
