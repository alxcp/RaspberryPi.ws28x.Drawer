from datetime import datetime
import random

from sources.effects.base import MatrixPixelEffect
from sources.helpers.color_rgb import ColorRGB


class FireEffect(MatrixPixelEffect):
    def __init__(self, drawer, width, height, frame_delay=0.3):
        MatrixPixelEffect.__init__(self, drawer, width, height, 1, frame_delay)
        self.sparks = []

    def play_frame(self):
        self.drawer.clear(False)

        for x in range(self.width):
            if random.randint(0, 1000) > 885:
                self.sparks.append(Spark(x))

        for spark in self.sparks:
            spark.process()

        to_remove = []

        for spark in self.sparks:
            if spark.altitude >= self.height:
                to_remove.append(spark)
            else:
                self.draw_spark(spark)

        for x in range(self.width):
            position = super(FireEffect, self).translate_to_matrix_columns(x, self.height - 1)
            color = ColorRGB(255, 0, 0)
            self.drawer.set_color(position, color)

        for r in to_remove:
            self.sparks.remove(r)

        self.drawer.show()

    def draw_spark(self, spark):
        for y in range(0, int(spark.altitude)):
            position = super(FireEffect, self).translate_to_matrix_columns(spark.position, self.height - 1 - y)
            color = ColorRGB(255 / ((y + 1) * 1), 0, 0)
            self.drawer.set_color(position, color)


class Spark(object):
    def __init__(self, position):
        self.position = position
        self.was_born = datetime.now()
        self.altitude = 0
        self.heat = 255
        self.color = ColorRGB(255, 0, 0)
        self.speed = random.randint(0, 10) / 10

    def process(self):
        t = datetime.now() - self.was_born
        self.altitude = self.altitude + self.speed

