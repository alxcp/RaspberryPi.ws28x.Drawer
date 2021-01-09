from datetime import datetime
import random

from effects.base import MatrixPixelEffect
from helpers.color_rgb import ColorRGB


class FireEffect(MatrixPixelEffect):
    def __init__(self, drawer, width, height, frame_delay=0.3):
        MatrixPixelEffect.__init__(self, drawer, width, height, 1, frame_delay)
        self.sparks = []

    def play_frame(self):
        self.drawer.clear(False)

        for x in range(self.width):
            if random.randint(0, 1000) > 885:
                self.sparks.append(Spark(x))

        for s in self.sparks:
            self.process_spark(s)

        to_remove = []

        for s in self.sparks:
            if s.altitude >= self.height:
                to_remove.append(s)
            else:
                self.draw_spark(s)

        for x in range(self.width):
            position = super(FireEffect, self).translate_to_matrix_columns(x, self.height - 1)
            color = ColorRGB(255, 0, 0)
            self.drawer.set_color(position, color)

        for r in to_remove:
            self.sparks.remove(r)

        self.drawer.show()

    def process_spark(self, spark):
        t = datetime.now() - spark.was_born
        spark.altitude = spark.altitude + spark.speed

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
