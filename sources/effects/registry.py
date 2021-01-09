import random
from datetime import timedelta

import sys
import traceback

from effects import different
from effects.fire import FireEffect
from effects.meteor_rain import MeteorRainEffect
from helpers.timeouts import Timeout
from helpers.timeouts import TimeoutInfinite


class PixelEffectsRegistry(object):
    effects = []
    current_effect_number = 0
    current_effect = None

    def __init__(self, drawer):
        self.drawer = drawer
        self.register(different.RainbowHSVEffect(drawer))
        self.register(different.RainbowHSV2Effect(drawer))
        self.register(different.BeadsEffect(drawer))
        self.register(different.RandomBlinksEffect(drawer))
        self.register(different.WavesEffect(drawer, 400, 4000))
        self.register(different.RainbowWavesEffect(drawer, 400, 4000))
        self.register(different.DropsEffect(drawer))
        self.register(MeteorRainEffect(drawer))
        self.register(FireEffect(drawer, 32, 8, 0))

    def register(self, effect):
        self.effects.append(effect)

    def play_effect(self, effect, timeout=None):
        self.current_effect = effect

        if timeout is None:
            timeout = TimeoutInfinite()

        try:
            effect.play(timeout)
        except KeyboardInterrupt:
            self.drawer.clear()

    def next_effect(self):
        self.current_effect_number = self.current_effect_number + 1
        if self.current_effect_number > len(self.effects) - 1:
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

            timeout = timedelta(seconds=random.randint(10, 10))

            print(f"\r\nWill run {next_effect} for a {timeout}")

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

            timeout = timedelta(seconds=10)

            print(f"\r\nWill run {next_effect} for a {timeout}")

            try:
                self.play_effect(next_effect, Timeout(timeout))
            except KeyboardInterrupt:
                self.drawer.clear()
                return
            except Exception as e:
                print(e)
