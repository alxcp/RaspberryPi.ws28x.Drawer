import random
import uuid
from configparser import ConfigParser
from datetime import timedelta, datetime

import sys
import traceback

import time

from sources.effects import different
from sources.effects.fire import FireEffect
from sources.effects.meteor_rain import MeteorRainEffect
from sources.helpers.timeouts import Timeout
from sources.helpers.timeouts import TimeoutInfinite


class PixelEffectsRegistry(object):
    effects = {}
    effect_keys = []
    current_effect_number = 0
    current_effect = None
    stop_requested = False
    cycle = None

    def __init__(self, drawer):
        self.config = read_config()

        self.drawer = drawer
        self.register(different.RainbowHSVEffect(drawer))
        self.register(different.RainbowHSV2Effect(drawer))
        self.register(different.BeadsEffect(drawer))
        self.register(different.RandomBlinksEffect(drawer))
        self.register(different.WavesEffect(drawer, 400, 4000))
        self.register(different.RainbowWavesEffect(drawer, 400, 4000))
        self.register(different.DropsEffect(drawer))
        self.register(MeteorRainEffect(drawer))
        self.register(FireEffect(drawer, 3, 32, 0))

        for key in self.effects.keys():
            self.effect_keys.append(key)

        self.effect_keys.sort()
        current_effect_name = self.config['effects_registry']['current_effect_name']
        self.current_effect_number = self.effect_keys.index(current_effect_name)
        self.current_effect = self.effects[current_effect_name]

    def register(self, effect, key=None):
        if key is None:
            key = effect.get_name()

        self.effects[key] = effect

    def play_effect(self, effect, timeout=None):
        self.current_effect = effect

        if timeout is None:
            timeout = TimeoutInfinite()

        try:
            self.play_routine(effect, timeout)
        except KeyboardInterrupt:
            self.drawer.clear()

    def play(self, timeout=None):
        self.play_effect(self.current_effect, timeout)

    def play_routine(self, effect, timeout):
        effect.started = datetime.now()
        self.config['effects_registry']['current_effect_name'] = effect.get_name()
        save_config(self.config)

        self.stop_requested = False
        frame_number = 0
        self.cycle = uuid.uuid4()
        current_cycle = self.cycle

        print('Playing {0} for {1} [{2}]'.format(effect.get_name(), timeout.get_display_name(), self.cycle))

        while not effect.is_stop(timeout) and not self.stop_requested and self.cycle == current_cycle:
            elapsed = (datetime.now() - effect.last_fps_populate).seconds
            if elapsed > 10:
                print('frame:{0}, fps: {1}'.format(frame_number, frame_number / elapsed))
                effect.last_fps_populate = datetime.now()
            effect.play_frame()
            if effect.frame_delay > 0:
                time.sleep(effect.frame_delay)
            frame_number = frame_number + 1
        print('end {0} [{1}]'.format(effect.get_name(), current_cycle))

    def play_next_effect(self):
        self.current_effect_number = self.current_effect_number + 1
        if self.current_effect_number > len(self.effect_keys) - 1:
            self.current_effect_number = 0

        next_effect = self.effects[self.effect_keys[self.current_effect_number]]

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

    def get_by_name(self, effect_name):
        for effect in self.effects:
            if effect.get_name() == effect_name:
                return effect
            else:
                print('{0} is not match'.format(effect.get_name()))

        return None

    def stop(self):
        self.stop_requested = True


def read_config():
    result = ConfigParser()
    result.read('settings.ini')

    is_changed = False

    if not result.has_section('effects_registry'):
        result.add_section('effects_registry')
        is_changed = True
    if not result.has_option('effects_registry', 'current_effect_name'):
        result['effects_registry']['current_effect_name'] = 'RainbowWavesEffect'
        is_changed = True

    if is_changed:
        save_config(result)

    return result


def save_config(config):
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
