import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
from colr import color

class ColorRGB(object):    
    def __init__(self, r = 0, g = 0, b = 0, drawer = None, correctGamma = None):
        if correctGamma and drawer is None:
            raise Exception("You need to provide drawer in order to use gamma correction")

        if correctGamma is None:
            if not drawer is None:
                correctGamma = drawer.CorrectGammaDefault                
            else:
                correctGamma = False

        if correctGamma:
            calibrationTable = drawer.CalibrationTable
            self.R = calibrationTable[int(r)]
            self.G = calibrationTable[int(g)]
            self.B = calibrationTable[int(b)]
        else:
            self.R = int(r)
            self.G = int(g)
            self.B = int(b)

    def multiply(self, k):
        r = self.R * k
        g = self.G * k
        b = self.B * k

        if r>255:
            r = 255
        if g>255:
            g = 255
        if b>255:
            b = 255

        return ColorRGB(r,g,b)

    def setComponent(self, channelNumber, value, drawer = None):
        r = 0
        g = 0
        b = 0

        if channelNumber == 0:
            r = value
        elif channelNumber == 1:
            g = value
        elif channelNumber == 2:
            b = value

        if not drawer is None:
            r = drawer.CalibrationTable[r]
            g = drawer.CalibrationTable[g]
            b = drawer.CalibrationTable[b]

        self.R = r
        self.G = g
        self.B = b

        

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

def getRandomColor(maxChannelCount=3, intensityMin = 0, intensityMax = 255, drawer=None):
    result = ColorRGB(drawer=drawer)
    if maxChannelCount == 1:
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax), drawer)
    elif maxChannelCount == 2:
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax), drawer)
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax), drawer)
    elif maxChannelCount == 3:
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax), drawer)
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax), drawer)
        result.setComponent(random.randint(0,2), random.randint(intensityMin, intensityMax), drawer)
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
