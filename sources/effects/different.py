import colorsys
import random
import math

from sources.helpers.color_rgb import ColorRGB
from sources.effects.base import PixelEffect


class RainbowHSVEffect(PixelEffect):
    def __init__(self, drawer, frame_delay=0):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.translate = 0
        self.p = 1.0 / (self.drawer.n_led * 1) * 1
        print(self.p)

    def play_frame(self):
        for z in self.drawer.pixels_indexes:
            pixel = colorsys.hsv_to_rgb((z + self.translate) * self.p, 1, 1)
            intens = self.drawer.intensity_max
            if random.randint(0, 5000) < 5:
                intens = 255

            self.drawer.set_color_raw(
                z,
                r=pixel[0] * intens,
                g=pixel[1] * intens,
                b=pixel[2] * intens)

        self.drawer.show()
        self.translate = self.translate + 1


class RainbowHSV2Effect(PixelEffect):
    def __init__(self, drawer, frame_delay=0):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.translate = 0
        self.translate_incr = 1
        self.p = 1.0 / (self.drawer.n_led * 5)

    def play_frame(self):
        for z in self.drawer.pixels_indexes:
            pixel = colorsys.hsv_to_rgb((z + self.translate) * self.p, 1, 1)
            self.drawer.set_color_raw(
                z,
                pixel[0] * self.drawer.intensity_max,
                pixel[1] * self.drawer.intensity_max,
                pixel[2] * self.drawer.intensity_max)

        self.drawer.show()

        if self.translate == self.drawer.n_led * 30:
            self.translate_incr = -1
        elif self.translate == 0:
            self.translate_incr = 1

        self.translate += self.translate_incr


class BeadsEffect(PixelEffect):
    def __init__(self, drawer, frame_delay=0):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.translate = 0
        self.step = 4
        self.wave_step = 0

        self.p = 1.0 / (drawer.n_led * 1) * 2
        self.total_wave_steps = drawer.intensity_max

    def play_frame(self):
        m = self.drawer.intensity_max * abs(math.sin(self.wave_step / self.total_wave_steps))

        for z in self.drawer.pixels_indexes:
            if (z - self.translate) % self.step == 0:
                pixel = colorsys.hsv_to_rgb((z + self.translate) * self.p, 1, 1)
                self.drawer.set_color_raw(z, pixel[0] * m, pixel[1] * m, pixel[2] * m)
            else:
                self.drawer.set_empty(z)

        self.wave_step += 1

        self.translate += 1
        self.drawer.show()


class RandomBlinksEffect(PixelEffect):
    def __init__(self, drawer, frame_delay=0):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.blinks = []
        self.max_leds = 10

    def play_frame(self):
        if len(self.blinks) < self.max_leds:
            blink_color = ColorRGB(
                random.randint(0, self.drawer.intensity_max),
                random.randint(0, self.drawer.intensity_max),
                random.randint(0, self.drawer.intensity_max))

            blink = Blink(random.randint(0, self.drawer.n_led - 1), blink_color, 10)
            self.blinks.append(blink)

        to_remove = []

        for blink in self.blinks:
            if not blink.next_step():
                to_remove.append(blink)

        for blink in to_remove:
            self.blinks.remove(blink)

        for z in range(0, self.drawer.n_led - 1):
            self.drawer.set_empty(z)

        for blink in self.blinks:
            self.drawer.set_color(blink.position, blink.current_color)

        self.drawer.show()


class ColorBounceEffect(PixelEffect):  # -m5-BOUNCE COLOR (SINGLE LED)
    def __init__(self, drawer, frame_delay=0.1):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.bounce_direction = 0
        self.index = 0

    def play_frame(self):
        if self.bounce_direction == 0:
            self.index = self.index + 1
            if self.index == self.drawer.n_led:
                self.bounce_direction = 1
                self.index = self.index - 1

        if self.bounce_direction == 1:
            self.index = self.index - 1
            if self.index == 0:
                self.bounce_direction = 0

        for i in range(0, self.drawer.n_led - 1):
            if i == self.index:
                self.drawer.set_color(i, ColorRGB.CHSV(self.drawer.n_led, i, self.drawer.intensity_max, 1))
            else:
                self.drawer.set_empty(i)

        self.drawer.show()


class FullFadeEffect(PixelEffect):
    def __init__(self, drawer, frame_delay=0.1):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.steps = 60
        self.current_step = 0
        self.bounce_direction = 1

    def play_frame(self):
        step_r = 0
        step_g = 0
        step_b = 0

        if self.current_step == self.steps - 30:
            self.bounce_direction = -1
        elif self.current_step == 0:
            self.bounce_direction = 1
            target_color = ColorRGB.random(2, self.drawer.intensity_min, self.drawer.intensity_max)

            step_r = target_color.r / float(self.steps)
            step_g = target_color.g / float(self.steps)
            step_b = target_color.b / float(self.steps)

        self.current_step += self.bounce_direction
        current_color = ColorRGB(
            step_r * self.current_step,
            step_g * self.current_step,
            step_b * self.current_step)

        for z in range(0, self.drawer.n_led - 1):
            self.drawer.set_color(z, current_color)

        self.drawer.show()


class WavesEffect(PixelEffect):
    def __init__(self, drawer, steps, cycles, frame_delay=0):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.steps = steps
        self.cycles = cycles
        self.current_step = 0
        self.current_cycle = 0
        self.transition_cycle = -1
        self.target_color = ColorRGB.random(2, drawer.intensity_min, drawer.intensity_max)
        self.target_transition_color = ColorRGB.random(2, drawer.intensity_min, drawer.intensity_max)

    def play_frame(self):
        if self.current_cycle >= self.cycles:
            if self.current_cycle == self.cycles:
                self.target_transition_color = ColorRGB.random(2, self.drawer.intensity_min, self.drawer.intensity_max)

            self.transition_cycle = self.current_cycle - self.cycles

            if self.transition_cycle == self.drawer.n_led:
                self.transition_cycle = -1
                self.target_color = self.target_transition_color
                self.current_cycle = 0

        self.current_cycle += 1
        self.current_step += 1

        for z in self.drawer.pixels_indexes:
            m = abs(math.sin((z + self.current_step) / self.steps))

            if z <= self.transition_cycle:
                c = self.target_transition_color
            else:
                c = self.target_color

            m_c = c.multiply(m, True)

            self.drawer.set_color(z, m_c)

        self.drawer.show()


class RainbowWavesEffect(PixelEffect):
    def __init__(self, drawer, steps, cycles, frame_delay=0.1):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.steps = steps
        self.cycles = cycles
        self.current_step = 0
        self.current_cycle = 0
        self.transition_cycle = 0
        self.p = 1.0 / (drawer.n_led * 5)

    def play_frame(self):
        if self.current_cycle >= self.cycles:
            self.transition_cycle += 1
            if self.current_cycle - self.cycles == self.drawer.n_led:
                self.current_cycle = 0

        self.current_cycle += 1
        self.current_step += 1

        for z in self.drawer.pixels_indexes:
            pixel = colorsys.hsv_to_rgb((z + self.transition_cycle) * self.p, 1, 1)

            m = abs(math.sin((z + self.current_step) / self.steps))
            c = ColorRGB(
                pixel[0] * self.drawer.intensity_max,
                pixel[1] * self.drawer.intensity_max,
                pixel[2] * self.drawer.intensity_max)
            m_c = c.multiply(m, True)
            self.drawer.set_color(z, m_c)

        self.drawer.show()


class DropsEffect(PixelEffect):
    def __init__(self, drawer, frame_delay=0):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.tail_len = 10
        self.drops_distance = 10
        self.drops = []

    def play_frame(self):
        drops_count = len(self.drops)
        if drops_count == 0:
            self.drops.append([0, ColorRGB.random(2, self.drawer.intensity_min, self.drawer.intensity_max)])
        elif self.drops[drops_count - 1][0] == self.tail_len + self.drops_distance:
            self.drops.append([0, ColorRGB.random(2, self.drawer.intensity_min, self.drawer.intensity_max)])

        delete_first = False

        for drop in self.drops:
            drop[0] = drop[0] + 1
            if drop[0] == self.drawer.n_led + self.tail_len:
                delete_first = True
            else:
                faid = self.tail_len
                for z in range(drop[0] - self.tail_len - 1 - self.drops_distance, drop[0]):
                    if 0 < z < self.drawer.n_led - 1:
                        if faid <= 0:
                            pixel = ColorRGB()
                        else:
                            pixel = drop[1].multiply(1 / float(faid))

                        self.drawer.set_color(z, pixel)
                        faid = faid - 1

        if delete_first:
            self.drops.remove(self.drops[0])

        self.drawer.show()


class Blink(object):
    def __init__(self, position, target_color, steps=5):
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
        if self.is_fading:
            self.step -= 1
        else:
            self.step += 1

        if self.step == 0:
            return False

        if self.step > self.steps:
            self.is_fading = True

        self.current_color = ColorRGB(
            self.incr_r * (self.step - 1),
            self.incr_g * (self.step - 1),
            self.incr_b * (self.step - 1))

        return True
