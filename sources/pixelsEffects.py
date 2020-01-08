import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
from colr import color

intensity = 20
calibrateTable = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1,  1,  1,  1, 1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2, 2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5, 5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36, 37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89, 90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114, 115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142, 144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175, 177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213, 215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255]

class ColorRGB(object):
    
    def __init__(self, r = 0, g = 0, b = 0, correctGamma = True):
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

#---FIND ADJACENT INDEX CLOCKWISE
def adjacent_cw(drawer, currentPosition):
  if currentPosition < drawer.nLED - 1:
    return currentPosition + 1
  else:
    return 0

#---FIND ADJACENT INDEX COUNTER-CLOCKWISE
def adjacent_ccw(drawer, currentPosition):
  if currentPosition > 0:
    return currentPosition - 1
  else:
    return drawer.nLED - 1

def CHSV(nLED, position, saturation, timesPerStripe = 1.0):
    p = 1.0 / nLED / timesPerStripe
    pixel = colorsys.hsv_to_rgb(position * p, 1, 1)
    return ColorRGB(pixel[0] * saturation, pixel[1] * saturation, pixel[2] * saturation)

def rainbow_hsv(drawer, timeout):
    translate = 0
    p = 1.0 / (drawer.nLED * 1) * 2
    print(p)

    while not timeout.IsExpired():
        for z in range(0,drawer.nLED - 1):
            pixel = colorsys.hsv_to_rgb((z + translate) * p, 1, 1)
            intens = intensity
            if random.randint(0,5000) < 5:
                intens = 255

            drawer.SetColor(z, ColorRGB(pixel[0] * intens, pixel[1] * intens, pixel[2] * intens))

        drawer.Show()
        translate = translate + 1
        time.sleep(0.03)

def stripes(drawer, timeout):
    nLED = drawer.nLED

    while not timeout.IsExpired():
        stripeLen = random.randint(0,nLED / 10)
        stripePos = random.randint(int(stripeLen /2),nLED - int(stripeLen/2))
        stripeR = random.randint(0,intensity)
        stripeG = random.randint(0,intensity)
        stripeB = random.randint(0,intensity)

        for z in range(0, int(stripeLen / 2)):
            drawer.SetColor(stripePos + z, ColorRGB(stripeR, stripeG, stripeB))
            drawer.SetColor(stripePos - z, ColorRGB(stripeR, stripeG, stripeB))
            drawer.Show()
            time.sleep(0.2)
        time.sleep(random.random())

def rainbow_hsv2(drawer, timeout):
    nLED = drawer.nLED
    translate = 0
    translateIncr = 1
    p = 1.0 / (nLED * 5)

    while not timeout.IsExpired():
        for z in range(nLED):
            pixel = colorsys.hsv_to_rgb((z + translate) * p, 1, 1)
            intens = intensity
            #if random.randint(0,50000) < 1:
            #    intens = 255
            drawer.SetColor(z, ColorRGB(pixel[0] * intens, pixel[1] * intens, pixel[2] * intens))
        drawer.Show()

        if translate==nLED * 30:
            translateIncr = -1
        elif translate == 0:
            translateIncr = 1

        translate = translate + translateIncr
        #time.sleep(0.03)

def beads(drawer, timeout):
    nLED = drawer.nLED
    translate = 0
    step = 4
    p = 1.0 / (nLED * 1) * 2
    intens = 1.0
    iinc = 0.5

    while not timeout.IsExpired():
        for z in range(nLED):
            if (z - translate) % step == 0:
                pixel = colorsys.hsv_to_rgb((z + translate)*p,1,1)
                drawer.SetColor(z, ColorRGB(pixel[0] * intens, pixel[1] * intens, pixel[2] * intens))
            else:
                drawer.SetColor(z, ColorRGB(0,0,0))
        intens=intens+iinc

        if intens>intensity or intens<1:
            iinc=iinc*-1
        
        translate=translate+1
        drawer.Show()
        time.sleep(0.4)

class Blink(object):
    def __init__(self, position, targetColor, steps = 5):
        self.Position = position
        self.Steps = steps
        self.Step = 0
        self.TargetColor = targetColor
        self.IncrR = targetColor.R / steps
        self.IncrG = targetColor.G / steps
        self.IncrB = targetColor.B / steps
        self.CurrentColor = ColorRGB(0,0,0)
        self.IsFading = False
        self.IsDone = False

    def NextStep(self):
        if (self.IsFading):
            self.Step = self.Step - 1
        else:
            self.Step = self.Step + 1

        if (self.Step == 0):
            return False

        if (self.Step > self.Steps):
            self.IsFading = True

        self.CurrentColor = ColorRGB(self.IncrR * (self.Step-1), self.IncrG * (self.Step-1), self.IncrB * (self.Step-1))
        return True

def randomBlinks(drawer, timeout):
    nLED = drawer.nLED
    blinks = []  
    maxLeds = 10  

    while not timeout.IsExpired():
        if (len(blinks)<maxLeds):
            blink = Blink(random.randint(0, nLED - 1),ColorRGB(random.randint(0,intensity), random.randint(0,intensity), random.randint(0, intensity)),10)
            blinks.append(blink)

        toRemove = []

        for blink in blinks:
            if (not blink.NextStep()):
                toRemove.append(blink)
        
        for blink in toRemove:
            blinks.remove(blink)

        for z in range(0, nLED - 1):
            drawer.SetColor(z, ColorRGB(0,0,0))
        
        for blink in blinks:
            drawer.SetColor(blink.Position, blink.CurrentColor)

        drawer.Show()
        time.sleep(0.2)

def color_bounce(drawer, timeout):                         #-m5-BOUNCE COLOR (SINGLE LED)
    bounceDirection = 0
    idex = 0

    while not timeout.IsExpired():
        if bounceDirection == 0:
            idex = idex + 1
            if idex == drawer.nLED:
                bounceDirection = 1
                idex = idex - 1
        if bounceDirection == 1:
            idex = idex - 1
            if idex == 0:
                bounceDirection = 0

        for i in range (0, drawer.nLED - 1):
            if i == idex:
                drawer.SetColor(i, CHSV(drawer.nLED, i, intensity, 1))
            else:
                drawer.SetColor(i, ColorRGB())

        drawer.Show()
        time.sleep(0.1)

def randomRed(drawer):
    temprand = 0
    nLED = drawer.nLED

    for i in range(0, nLED - 1):
        temprand = random.randint(0, 100)
        if temprand > 50:
            drawer.SetColor(i, ColorRGB(intensity, 0, 0))
        if temprand <= 50:
            drawer.SetColor(i, ColorRGB())

    drawer.Show()

def rule30(drawer, timeout):                          #-m13-1D CELLULAR AUTOMATA - RULE 30 (RED FOR NOW)
    bounceDirection = 0

    while not timeout.IsExpired():
        if bounceDirection == 0:
            randomRed(drawer)
            bounceDirection = 1

        copy = drawer.GetCopy()
        iCW = 0
        iCCW = 0
        y = 100
        for i in range(0, drawer.nLED - 1):
            iCW = adjacent_cw(drawer, i)
            iCCW = adjacent_ccw(drawer, i)
            if copy[iCCW].R > y and copy[i].R > y and copy[iCW].R > y:
                drawer.SetColor(i, ColorRGB())
            if copy[iCCW].R > y and copy[i].R > y and copy[iCW].R <= y:
                drawer.SetColor(i, ColorRGB())
            if copy[iCCW].R > y and copy[i].R <= y and copy[iCW].R > y:
                drawer.SetColor(i, ColorRGB())
            if copy[iCCW].R > y and copy[i].R <= y and copy[iCW].R <= y:
                drawer.SetColor(i, ColorRGB(255))
            if copy[iCCW].R <= y and copy[i].R > y and copy[iCW].R > y:
                drawer.SetColor(i, ColorRGB(255))
            if copy[iCCW].R <= y and copy[i].R > y and copy[iCW].R <= y:
                drawer.SetColor(i, ColorRGB(255))
            if copy[iCCW].R <= y and copy[i].R <= y and copy[iCW].R > y:
                drawer.SetColor(i, ColorRGB(255))
            if copy[iCCW].R <= y and copy[i].R <= y and copy[iCW].R <= y:
                drawer.SetColor(i, ColorRGB())
        drawer.Show()
        time.sleep(0.5)

def fullFade(drawer, timeout):
    steps = 60
    currentStep = 0
    bounceDirection = 1

    while not timeout.IsExpired():
        if currentStep == steps - 30:
            bounceDirection = -1
        elif currentStep == 0:
            bounceDirection = 1
            targetColor = getRandomPredefinedColor()
                
            stepR = targetColor.R / float(steps)
            stepG = targetColor.G / float(steps)
            stepB = targetColor.B / float(steps)


        currentStep = currentStep + bounceDirection
        currentColor = ColorRGB(stepR * currentStep, stepG * currentStep, stepB * currentStep)

        for z in range(0, drawer.nLED -1):
            drawer.SetColor(z, currentColor)
        drawer.Show()
        time.sleep(0.1)

def waves(drawer, timeout):
    steps = 100
    currentStep = 0
    cycles = 400
    currentCycle = 0
    colorTransitionCycles = 200
    targetColor = getRandomColor(2,10,100)
    targetTransitColor = targetColor
    stepsCache = []
    transitionCycle = -1

    while not timeout.IsExpired():
        if currentCycle >= cycles:
            if currentCycle == cycles:
                targetTransitionColor = getRandomColor(2,30,100)
                print ("prevColor: " + targetColor.ToString() + ", ttr: " + targetTransitionColor.ToString())

            transitionCycle = currentCycle - cycles
            
            if transitionCycle == drawer.nLED:
                transitionCycle = -1
                targetColor = targetTransitionColor                
                currentCycle = 0

        currentCycle = currentCycle + 1
        currentStep = currentStep + 1

        for z in range(0, drawer.nLED -1):
            m = abs(math.sin((z + currentStep) / steps))
            
            if z <= transitionCycle:                
                c = targetTransitionColor
            else:
                c = targetColor

            mC = c.multiply(m)
                
            if mC.R == 0 and c.R > 0:
                mC.R = 1
            if mC.G == 0 and c.G > 0:
                mC.G = 1
            if mC.B == 0 and c.B > 0:
                mC.B = 1
            drawer.SetColor(z, mC)
            
        drawer.Show()

def randomReplacement(drawer, timeout):
    steps = 60
    currentStep = 0

    while not timeout.IsExpired():
        targetColor = getRandomPredefinedColor()
                
        stepR = targetColor.R / float(steps)
        stepG = targetColor.G / float(steps)
        stepB = targetColor.B / float(steps)

        order = []
        for z in range(0, drawer.nLED - 1):
            order.append(z)
        
        random.shuffle(order)        

        currentStep = 7
        currentColor = ColorRGB(stepR * currentStep, stepG * currentStep, stepB * currentStep)

        for z in order:
            drawer.SetColor(z, currentColor)
            drawer.Show()

def switchColors(drawer, timeout):
    firstColor = ColorRGB(255,153,51).multiply(0.1)
    secondColor = ColorRGB(102, 153, 255).multiply(0.1)
    step = 0

    while not timeout.IsExpired():
        if step == 1:
            step = 2
        else:
            step = 1

        for ln in range(0,drawer.nLED-1,3):
            if step == 1:
                drawer.SetColor(ln, firstColor)
                drawer.SetColor(ln+1,secondColor)
                drawer.SetColor(ln+2,secondColor)
            else:
                drawer.SetColor(ln, secondColor)
                drawer.SetColor(ln+1, firstColor)
                drawer.SetColor(ln+2, firstColor)
        drawer.Show()
        time.sleep(1)

def drops(drawer, timeout):
    tailLen = 10
    dropsDistance = 10
    drops = []

    while not timeout.IsExpired():
        dropsCount = len(drops)
        if dropsCount == 0:
            drops.append([0, getRandomPredefinedColor().multiply(0.9)])
        elif drops[dropsCount - 1][0] == tailLen + dropsDistance:
            drops.append([0, getRandomPredefinedColor().multiply(0.9)])
        
        deleteFirst = False

        for drop in drops:
            drop[0] = drop[0]+1
            if drop[0] == drawer.nLED + tailLen:
                deleteFirst = True
            else:
                faid = tailLen
                for z in range(drop[0] - tailLen - 1 - dropsDistance, drop[0]):
                    if z > 0 and z < drawer.nLED - 1:
                        if faid <= 0:
                            pixel = ColorRGB()
                        else:
                            pixel = drop[1].multiply(1/float(faid))

                        #print (str(z) + ": " + str(pixel.R) + " " + str(pixel.G) + " " + str(pixel.B))
                        
                        drawer.SetColor(z, pixel)
                        faid = faid - 1
        
        if deleteFirst:
            drops.remove(drops[0])

        drawer.Show()
        time.sleep(0.1)

def fill(drawer, timeout):

    step = 0
    while not timeout.IsExpired():
        if step == 0:
            for z in range(0,255-1):
                drawer.SetColor(z, ColorRGB(z,0,0))
            drawer.Show()
            step = 1
        elif step == 1:
            for z in range(0,255-1):
                drawer.SetColor(z, ColorRGB(0,z,0))
            drawer.Show()
            step = 2
        elif step == 2:
            for z in range(0,255-1):
                drawer.SetColor(z, ColorRGB(0,0,z))
            drawer.Show()
            step = 0
        time.sleep(10)

def thread(drawer, timeout):
    for lastNumber in range(drawer.nLED - 1, 0, -1):
        ledColor = getRandomColor(2,3,20)
        for ledNumber in range(1,lastNumber):
            drawer.SetColor(ledNumber,ledColor)
            drawer.SetColor(ledNumber-1,ColorRGB())
            drawer.Show()

def thread2(drawer, timeout):
    nCL=int(drawer.nLED/2)
    for lastNumber in range(1,nCL- 1):
        ledColor = getRandomColor(2,3,20)
        for ledNumber in range(1,nCL - lastNumber):            
            drawer.SetColor(nCL-ledNumber,ledColor)
            drawer.SetColor(nCL-ledNumber+1,ColorRGB())
            drawer.SetColor(nCL+ledNumber,ledColor)
            drawer.SetColor(nCL+ledNumber-1,ColorRGB())
            drawer.Show()
            
            
def skittles(drawer, timeout):
    while not timeout.IsExpired():
        for z in range(0,drawer.nLED-1):
            drawer.SetColor(z, getRandomColor(2,3,20))
        drawer.Show()
        time.sleep(3)
        

def runWithDrawer(drawer, effect, timeout = None):

    if timeout is None:
        timeout = TimeoutInfinite()
    
    try:
        effect(drawer, timeout)
    except KeyboardInterrupt:
        drawer.Clear()

def runRandomized(drawer):

    while True:
        nextEffectNumber = random.randint(1,8)
        if nextEffectNumber == 1:
            nextEffect = drops          #1
        elif nextEffectNumber == 2:
            nextEffect = color_bounce    #2
        elif nextEffectNumber == 3:
            nextEffect = randomBlinks    #3
        elif nextEffectNumber == 4:
            nextEffect = beads           #4
        elif nextEffectNumber == 5:
            nextEffect = rainbow_hsv2    #5
        elif nextEffectNumber == 6:
            nextEffect = fullFade    #6
        elif nextEffectNumber == 7:
            nextEffect = randomReplacement    #7
        elif nextEffectNumber == 8:
            nextEffect = switchColors    #8
        else:
            nextEffect = stripes         #8

        timeout = timedelta(seconds=random.randint(20,120))

        print ("Will run " + str(nextEffect) + " for a " + str(timeout))

        try:
            runWithDrawer(drawer, nextEffect, Timeout(timeout))
        except KeyboardInterrupt:
            drawer.Clear()
            return
        except:
            print ("Exception")

