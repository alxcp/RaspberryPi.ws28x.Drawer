import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
from colr import color

intensityMin = 4
intensity = 20
calibrateTable = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1,  1,  1,  1, 1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2, 2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5, 5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36, 37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89, 90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114, 115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142, 144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175, 177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213, 215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255]
correctGammaDefault = True

class ColorRGB(object):
    
    def __init__(self, r = 0, g = 0, b = 0, correctGamma = None):
        if correctGamma is None:
            correctGamma = correctGammaDefault

        if correctGamma:
            self.R = calibrateTable[int(r)]
            self.G = calibrateTable[int(g)]
            self.B = calibrateTable[int(b)]
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

    def setComponent(self, channelNumber, value):
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

def getRandomColor(maxChannelCount=3, minIntensity = 0, maxIntensity = 255):
    result = ColorRGB()
    if maxChannelCount == 1:
        result.setComponent(random.randint(0,2), random.randint(minIntensity, maxIntensity))
    elif maxChannelCount == 2:
        result.setComponent(random.randint(0,2), random.randint(minIntensity, maxIntensity))
        result.setComponent(random.randint(0,2), random.randint(minIntensity, maxIntensity))
    elif maxChannelCount == 3:
        result.setComponent(random.randint(0,2), random.randint(minIntensity, maxIntensity))
        result.setComponent(random.randint(0,2), random.randint(minIntensity, maxIntensity))
        result.setComponent(random.randint(0,2), random.randint(minIntensity, maxIntensity))
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
