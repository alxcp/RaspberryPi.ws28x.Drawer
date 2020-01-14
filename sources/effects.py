import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
import helpers
from helpers import Timeout
from helpers import TimeoutInfinite
from helpers import ColorRGB
from helpers import PixelEffect

class PixelEffectsRegistry(object):
    effects = []

    def __init__(self):
        self.register(RainbowHSVEffect())
        self.register(RainbowHSV2Effect())
        self.register(StripesEffect())
        self.register(BeadsEffect())
        self.register(RandomBlinksEffect())
        self.register(FullFadeEffect())
        self.register(WavesEffect(400, 4000))
        self.register(RainbowWavesEffect(400, 4000))
        self.register(RandomReplacementEffect())
        self.register(DropsEffect())
        self.register(FillEffect())

    def register(self, effect):
        self.effects.append(effect)

    def play_effect(self, drawer, effect, timeout = None):
        if timeout is None:
            timeout = TimeoutInfinite()

        try:
            effect.play(drawer, timeout)
        except KeyboardInterrupt:
            drawer.clear()

    def play_randomized_effect(self, drawer):
        while True:
            next_effect_index = random.randint(0, len(self.effects) - 1)
            next_effect = self.effects[next_effect_index]

            timeout = timedelta(seconds = random.randint(20, 120))

            print (f"\rWill run {next_effect} for a {timeout}\r")

            try:
                self.play_effect(drawer, next_effect, Timeout(timeout))
            except KeyboardInterrupt:
                drawer.clear()
                return
            except:
                print ("Exception")

    def demo(self, drawer):
        next_effect_index = -1

        while True:
            next_effect_index += 1
            if next_effect_index >= len(self.effects):
                next_effect_index = 0

            next_effect = self.effects[next_effect_index]

            timeout = timedelta(seconds = 10)

            print (f"\rWill run {next_effect} for a {timeout}\r")

            try:
                self.play_effect(drawer, next_effect, Timeout(timeout))
            except KeyboardInterrupt:
                drawer.clear()
                return
            except Exception as e:
                print(e)

class RainbowHSVEffect(PixelEffect):
    def play(self, drawer, timeout):
        translate = 0
        p = 1.0 / (drawer.nLED * 1) * 2
        print(p)

        while not timeout.is_expired():
            for z in drawer.pixels_indexes:
                pixel = colorsys.hsv_to_rgb((z + translate) * p, 1, 1)
                intens = drawer.intensity_max
                if random.randint(0, 5000) < 5:
                    intens = 255

                drawer.set_color_raw(
                    z, 
                    r = pixel[0] * intens, 
                    g = pixel[1] * intens, 
                    b = pixel[2] * intens)

            drawer.show()
            translate = translate + 1
            time.sleep(0.03)

class StripesEffect(PixelEffect):
    def play(self, drawer, timeout):
        nLED = drawer.nLED
        intensity = drawer.intensity_max

        while not timeout.is_expired():
            stripeLen = random.randint(0, nLED / 10)
            stripePos = random.randint(int(stripeLen /2), nLED - int(stripeLen/2))
            stripeR = random.randint(0, intensity)
            stripeG = random.randint(0, intensity)
            stripeB = random.randint(0, intensity)

            for z in range(0, int(stripeLen / 2)):
                drawer.set_color_raw(stripePos + z, stripeR, stripeG, stripeB)
                drawer.set_color_raw(stripePos - z, stripeR, stripeG, stripeB)
                drawer.show()
                time.sleep(0.2)

class RainbowHSV2Effect(PixelEffect):
    def play(self, drawer, timeout):
        nLED = drawer.nLED
        translate = 0
        translate_incr = 1
        p = 1.0 / (nLED * 5)
        intensity = drawer.intensity_max

        while not timeout.is_expired():
            for z in drawer.pixels_indexes:
                pixel = colorsys.hsv_to_rgb((z + translate) * p, 1, 1)
                drawer.set_color_raw(
                    z, 
                    pixel[0] * intensity, 
                    pixel[1] * intensity, 
                    pixel[2] * intensity)
            drawer.show()

            if translate == nLED * 30:
                translate_incr = -1
            elif translate == 0:
                translate_incr = 1

            translate += translate_incr

class BeadsEffect(PixelEffect):
    def play(self, drawer, timeout):
        nLED = drawer.nLED
        translate = 0
        step = 4
        p = 1.0 / (nLED * 1) * 2
        intensity = drawer.intensity_max
        wave_step = 0
        total_wave_steps = drawer.intensity_max
        

        while not timeout.is_expired():
            m = intensity * abs(math.sin((wave_step) / total_wave_steps))

            for z in drawer.pixels_indexes:
                if (z - translate) % step == 0:
                    pixel = colorsys.hsv_to_rgb((z + translate) * p, 1, 1)
                    drawer.set_color_raw(z, pixel[0] * m, pixel[1] * m, pixel[2] * m)
                else:
                    drawer.set_empty(z)

            wave_step += 1

            translate += 1
            drawer.show()
            time.sleep(0.1)

class Blink(object):
    def __init__(self, position, target_color, steps = 5):
        self.position = position
        self.steps = steps
        self.step = 0
        self.target_color = target_color
        self.incr_r = target_color.r / steps
        self.incr_g = target_color.g / steps
        self.incr_b = target_color.b / steps
        self.current_color = ColorRGB()
        self.is_fading = False
        self.is_done = False

    def next_step(self):
        if (self.is_fading):
            self.step -= 1
        else:
            self.step += 1

        if (self.step == 0):
            return False

        if (self.step > self.steps):
            self.is_fading = True

        self.current_color = ColorRGB(
            self.incr_r * (self.step - 1), 
            self.incr_g * (self.step - 1), 
            self.incr_b * (self.step - 1))

        return True

class RandomBlinksEffect(PixelEffect):
    def play(self, drawer, timeout):
        nLED = drawer.nLED
        blinks = []  
        maxLeds = 10  
        intensity = drawer.intensity_max

        while not timeout.is_expired():
            if (len(blinks) < maxLeds):
                blink_color = ColorRGB(
                            random.randint(0, intensity), 
                            random.randint(0, intensity), 
                            random.randint(0, intensity))

                blink = Blink(random.randint(0, nLED - 1), blink_color, 10)
                blinks.append(blink)

            to_remove = []

            for blink in blinks:
                if (not blink.next_step()):
                    to_remove.append(blink)
            
            for blink in to_remove:
                blinks.remove(blink)

            for z in range(0, nLED - 1):
                drawer.set_empty(z)
            
            for blink in blinks:
                drawer.set_color(blink.position, blink.current_color)

            drawer.show()
            time.sleep(0.2)

class ColorBounceEffect(PixelEffect):                         #-m5-BOUNCE COLOR (SINGLE LED)
    def play(self, drawer, timeout):    
        bounce_direction = 0
        idex = 0
        intensity = drawer.intensity_max

        while not timeout.is_expired():
            if bounce_direction == 0:
                idex = idex + 1
                if idex == drawer.nLED:
                    bounce_direction = 1
                    idex = idex - 1

            if bounce_direction == 1:
                idex = idex - 1
                if idex == 0:
                    bounce_direction = 0

            for i in range (0, drawer.nLED - 1):
                if i == idex:
                    drawer.set_color(i, ColorRGB.CHSV(drawer.nLED, i, intensity, 1))
                else:
                    drawer.set_empty(i)

            drawer.show()
            time.sleep(0.1)

class FullFadeEffect(PixelEffect):
    def play(self, drawer, timeout):
        steps = 60
        current_step = 0
        bounce_direction = 1

        while not timeout.is_expired():
            if current_step == steps - 30:
                bounce_direction = -1
            elif current_step == 0:
                bounce_direction = 1
                targetColor = ColorRGB.random(2, drawer.intensity_min, drawer.intensity_max)
                    
                stepR = targetColor.r / float(steps)
                stepG = targetColor.g / float(steps)
                stepB = targetColor.b / float(steps)

            current_step += bounce_direction
            currentColor = ColorRGB(
                stepR * current_step, 
                stepG * current_step, 
                stepB * current_step)

            for z in range(0, drawer.nLED - 1):
                drawer.set_color(z, currentColor)

            drawer.show()
            time.sleep(0.1)

class WavesEffect(PixelEffect):
    def __init__(self, steps, cycles):
        self.steps = steps
        self.cycles = cycles

    def play(self, drawer, timeout):
        current_step = 0
        current_cycle = 0
        intensity_min = drawer.intensity_min
        intensity_max = drawer.intensity_max
        target_color = ColorRGB.random(2, intensity_min, intensity_max)
        transition_cycle = -1

        while not timeout.is_expired():
            if current_cycle >= self.cycles:
                if current_cycle == self.cycles:
                    target_transition_color = ColorRGB.random(2, intensity_min, intensity_max)

                transition_cycle = current_cycle - self.cycles
                
                if transition_cycle == drawer.nLED:
                    transition_cycle = -1
                    target_color = target_transition_color
                    current_cycle = 0

            current_cycle += 1
            current_step += 1

            for z in drawer.pixels_indexes:
                m = abs(math.sin((z + current_step) / self.steps))
                
                if z <= transition_cycle:
                    c = target_transition_color
                else:
                    c = target_color

                mC = c.multiply(m)
                    
                if mC.r == 0 and c.r > 0:
                    mC.r = 1
                if mC.g == 0 and c.g > 0:
                    mC.g = 1
                if mC.b == 0 and c.b > 0:
                    mC.b = 1
                drawer.set_color(z, mC)
                
            drawer.show()

class RainbowWavesEffect(PixelEffect):
    def __init__(self, steps, cycles):
        self.steps = steps
        self.cycles = cycles

    def play(self, drawer, timeout):
        current_step = 0
        current_cycle = 0
        transition_cycle = -1
        p = 1.0 / (drawer.nLED * 5)
        
        while not timeout.is_expired():
            if current_cycle >= self.cycles:
                transition_cycle += 1
                if current_cycle - self.cycles == drawer.nLED:
                    current_cycle = 0

            current_cycle += 1
            current_step += 1

            for z in drawer.pixels_indexes:
                pixel = colorsys.hsv_to_rgb((z + transition_cycle) * p, 1, 1)

                m = abs(math.sin((z + current_step) / self.steps))
                c = ColorRGB(
                    pixel[0] * drawer.intensity_max, 
                    pixel[1] * drawer.intensity_max, 
                    pixel[2] * drawer.intensity_max)
                mC = c.multiply(m, True)
                drawer.set_color(z, mC)
                
            drawer.show()

class RandomReplacementEffect(PixelEffect):
    def play(self, drawer, timeout):
        order = []
        for z in drawer.pixels_indexes:
            order.append(z)

        while not timeout.is_expired():
            target_color = ColorRGB.random(2, drawer.intensity_min, drawer.intensity_max)
            
            random.shuffle(order)

            for z in order:
                drawer.set_color(z, target_color)
                drawer.show()

class DropsEffect(PixelEffect):
    def play(self, drawer, timeout):
        tail_len = 10
        drops_distance = 10
        drops = []

        while not timeout.is_expired():
            drops_count = len(drops)
            if drops_count == 0:
                drops.append([0, ColorRGB.random(2, drawer.intensity_min, drawer.intensity_max)])
            elif drops[drops_count - 1][0] == tail_len + drops_distance:
                drops.append([0, ColorRGB.random(2, drawer.intensity_min, drawer.intensity_max)])
            
            delete_first = False

            for drop in drops:
                drop[0] = drop[0]+1
                if drop[0] == drawer.nLED + tail_len:
                    delete_first = True
                else:
                    faid = tail_len
                    for z in range(drop[0] - tail_len - 1 - drops_distance, drop[0]):
                        if z > 0 and z < drawer.nLED - 1:
                            if faid <= 0:
                                pixel = ColorRGB()
                            else:
                                pixel = drop[1].multiply(1 / float(faid))
                            
                            drawer.set_color(z, pixel)
                            faid = faid - 1
            
            if delete_first:
                drops.remove(drops[0])

            drawer.show()
            time.sleep(0.1)

class FillEffect(PixelEffect):
    def play(self, drawer, timeout):
        step = 0
        while not timeout.is_expired():
            if step == 0:
                for z in range(0, 255 - 1):
                    drawer.set_color(z, ColorRGB(z, 0, 0))
                drawer.show()
                step = 1
            elif step == 1:
                for z in range(0, 255 - 1):
                    drawer.set_color(z, ColorRGB(0, z, 0))
                drawer.show()
                step = 2
            elif step == 2:
                for z in range(0, 255 - 1):
                    drawer.set_color(z, ColorRGB(0, 0, z))
                drawer.show()
                step = 0
            time.sleep(10)

class ThreadEffect(PixelEffect):
    def play(self, drawer, timeout):
        for last_number in range(drawer.nLED - 1, 0, -1):
            ledColor = ColorRGB.random(2, 3, 20)
            if timeout.is_expired:
                return
            for led_number in range(1, last_number):
                drawer.set_color(led_number, ledColor)
                drawer.set_empty(led_number - 1)
                drawer.show()

class Thread2Effect(PixelEffect):
    def play(self, drawer, timeout):
        nCL = int(drawer.nLED / 2)
        for last_number in range(1, nCL - 1):
            ledColor = ColorRGB.random(2, 3, 20)
            if timeout.is_expired:
                return
            for led_number in range(1,nCL - last_number):
                drawer.set_color(nCL - led_number, ledColor)
                drawer.set_empty(nCL - led_number + 1)
                drawer.set_color(nCL + led_number, ledColor)
                drawer.set_empty(nCL + led_number - 1)
                drawer.show()