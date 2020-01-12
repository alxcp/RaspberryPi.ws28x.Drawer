import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
from colr import color


class DrawerBase(object):
    CalibrationTable = [range(0,255)]
    CorrectGammaDefault = False
    IntensityMin = 170
    IntensityMax = 255

    def __init__(self, nLED):
        self.nLED = nLED

    def SetColor(self, position, color, calibrate = None):
        raise NotImplementedError()

    def Show(self):
        raise NotImplementedError()

    def Clear(self):
        raise NotImplementedError()

    def GetCopy(self):
        raise NotImplementedError()

    def CalibrateColor(self, color):
        return ColorRGB(self.CalibrationTable[color.R], self.CalibrationTable[color.G], self.CalibrationTable[color.B])


class ColorRGB(object):    
    def __init__(self, r = 0, g = 0, b = 0):
        self.R = int(r)
        self.G = int(g)
        self.B = int(b)

    def multiply(self, k, doNotLooseComponents = False):
        r = min(int(self.R * k), 255)
        g = min(int(self.G * k), 255)
        b = min(int(self.B * k), 255)

        if doNotLooseComponents:
            if self.R > 0 and r == 0:
                r = 1
            if self.G > 0 and g == 0:
                g = 1
            if self.B > 0 and b == 0:
                b = 1

        return ColorRGB(r, g, b)

    def setComponent(self, channelNumber, value, drawer = None):
        if channelNumber == 0:
            self.R = value
        elif channelNumber == 1:
            self.G = value
        elif channelNumber == 2:
            self.B = value

    def ToString(self):
        return "(" + str(self.R) + ", " + str(self.G) + ", " + str(self.B) + ")"


class Timeout(object):
    def __init__(self, delta):
        self.EndTime = datetime.now() + delta

    def IsExpired(self):
        return datetime.now() > self.EndTime

class TimeoutInfinite(object):
    def IsExpired(self):
        return False

def getRandomColor(maxChannelCount=3, intensityMin = 0, intensityMax = 255):
    result = ColorRGB()
    if maxChannelCount == 1:
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax))
    elif maxChannelCount == 2:
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax))
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax))
    elif maxChannelCount == 3:
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax))
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax))
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax))
    return result

def getRandomPredefinedColor():
    c = random.randint(0,8)

    if c == 0:
        targetColor = ColorRGB(255,215,0)
    elif c == 1:
        targetColor = ColorRGB(220,20,60)
    elif c == 2:
        targetColor = ColorRGB(255,140,0)
    elif c == 3:
        targetColor = ColorRGB(34,139,34)
    elif c == 4:
        targetColor = ColorRGB(0,0,128)
    elif c == 5:
        targetColor = ColorRGB(106,90,205)
    elif c == 6:
        targetColor = ColorRGB(244,164,96)
    elif c == 7:
        targetColor = ColorRGB(128,0,128)
    elif c == 8:
        targetColor = ColorRGB(123,104,238)
    else:
        targetColor = ColorRGB(20,100,200)
    
    return targetColor

def CHSV(nLED, position, saturation, timesPerStripe = 1.0):
    p = 1.0 / nLED / timesPerStripe
    pixel = colorsys.hsv_to_rgb(position * p, 1, 1)
    return ColorRGB(pixel[0] * saturation, pixel[1] * saturation, pixel[2] * saturation)
