from datetime import datetime
import time


class PixelEffect(object):
    def __init__(self, drawer, frame_delay=0.1):
        self.frame_delay = frame_delay
        self.started = None
        self.last_fps_populate = datetime.now()
        self.drawer = drawer
        print('Frame Delay: {0}'.format(frame_delay))

    def is_stop(self, timeout):
        result = timeout.is_expired()  # or self.drawer.stop_requested
        # self.drawer.stop_requested = False
        return result

    def play_frame(self):
        raise NotImplementedError()

    def get_name(self):
        return self.__class__.__name__


class MatrixPixelEffect(PixelEffect):
    def __init__(self, drawer, width, height, blocks, frame_delay):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.width = width
        self.height = height
        self.blocks = blocks
        self.block_length = width * height

    def translate_to_matrix_rows(self, x, y):
        current_block = x // self.width
        block_shift = current_block * self.block_length

        x = x - current_block * self.width

        if (y % 2) == 0:
            return y * self.width - x - 1 + block_shift
        else:
            return (y - 1) * self.width + x + block_shift

    def translate_to_matrix_columns(self, x, y):
        current_block = y // self.height
        block_shift = current_block * self.block_length

        y = y - current_block * self.height

        if (x % 2) == 0:
            return x * self.height - y - 1 + block_shift
        else:
            return (x - 1) * self.height + y + block_shift
