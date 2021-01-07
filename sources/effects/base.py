from datetime import datetime
from datetime import timedelta

class PixelEffect(object):
    def __init__(self, drawer, frame_delay = 0.1):
        self.frame_delay = frame_delay
        self.started = None
        self.last_fps_populate = datetime.now()
        self.drawer = drawer
        print('Frame Delay: {0}'.format(frame_delay))
        
    def is_stop(self, timeout):
        result = timeout.is_expired() or self.drawer.stop_requested
        self.drawer.stop_requested = False
        return result
    
    def play(self, timeout):
        self.started = datetime.now()
        print('Playing {0} for {1}'.format(self.__class__.__name__, timeout))
        frame_number = 0
        while not self.is_stop(timeout):
            elapsed = (datetime.now() - self.last_fps_populate).seconds
            if (elapsed > 10):
                print('frame:{0}, fps: {1}'.format(frame_number, frame_number / elapsed))
                self.last_fps_populate = datetime.now()
            self.play_frame()
            if self.frame_delay > 0:
                time.sleep(self.frame_delay)
            frame_number = frame_number + 1
        print('end')
    
    def play_frame(self):
        raise NotImplementedError()

class MatrixPixelEffect(PixelEffect):
    def __init__(self, drawer, width, height, blocks, frame_delay):
        PixelEffect.__init__(self, drawer, frame_delay)
        self.width = width
        self.height = height
        self.blocks = blocks
        self.block_length = width * height
           
    def translateToMatrixRows(self, x, y):
        current_block = x // self.width
        block_shift = current_block * self.block_length
        
        x = x - current_block * self.width
        
        if (y % 2) == 0:
            return y * self.width - x - 1 + block_shift
        else:
            return (y - 1) * self.width + x + block_shift
        
    def translateToMatrixColumns(self, x, y):
        current_block = y // self.height
        block_shift = current_block * self.block_length
        
        y = y - current_block * self.height
        
        if (x % 2) == 0:
            return x * self.height - y - 1 + block_shift
        else:
            return (x - 1) * self.height + y + block_shift