import time
from datetime import datetime
from datetime import timedelta
import colorsys
import random
import math
from colr import color
import helpers
from helpers import *

class PixelEffectsRegistry(object):
    Effects = []

    def __init__(self):
        self.Register(RainbowHSVEffect())
        self.Register(RainbowHSV2Effect())
        self.Register(StripesEffect())
        self.Register(BeadsEffect())
        self.Register(RandomBlinksEffect())
        self.Register(FullFadeEffect())
        self.Register(WavesEffect(400, 4000))
        self.Register(RandomReplacementEffect())
        self.Register(SwitchColorsEffect())
        self.Register(DropsEffect())
        self.Register(FillEffect())
        self.Register(Thread())
        self.Register(Thread2())
        self.Register(Skittles())

    def Register(self, effect):
        self.Effects.append(effect)

    def PlayEffect(self, drawer, effect, timeout = None):
        if timeout is None:
            timeout = TimeoutInfinite()        

        try:
            effect.Play(drawer, timeout)
        except KeyboardInterrupt:
            drawer.Clear()

    def PlayRandomizedEffect(self, drawer):
        while True:
            nextEffectNumber = random.randint(0,len(self.Effects) - 1)
            nextEffect = self.Effects[nextEffectNumber]

            timeout = timedelta(seconds=random.randint(20,120))

            print ("Will run " + str(nextEffect) + " for a " + str(timeout))

            try:
                self.PlayEffect(drawer, nextEffect, Timeout(timeout))
            except KeyboardInterrupt:
                drawer.Clear()
                return
            except:
                print ("Exception")

class PixelEffect(object):
    def Play(self, drawer, timeout):
        raise NotImplementedError()


class RainbowHSVEffect(PixelEffect):
    def Play(self, drawer, timeout):
        translate = 0
        p = 1.0 / (drawer.nLED * 1) * 2
        print(p)

        while not timeout.IsExpired():
            for z in range(0,drawer.nLED - 1):
                pixel = colorsys.hsv_to_rgb((z + translate) * p, 1, 1)
                intens = drawer.IntensityMax
                if random.randint(0,5000) < 5:
                    intens = 255

                drawer.SetColor(z, ColorRGB(pixel[0] * intens, pixel[1] * intens, pixel[2] * intens))

            drawer.Show()
            translate = translate + 1
            time.sleep(0.03)

class StripesEffect(PixelEffect):
    def Play(self, drawer, timeout):
        nLED = drawer.nLED
        intensity = drawer.IntensityMax

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

class RainbowHSV2Effect(PixelEffect):
    def Play(self, drawer, timeout):
        nLED = drawer.nLED
        translate = 0
        translateIncr = 1
        p = 1.0 / (nLED * 5)
        intensity = drawer.IntensityMax

        while not timeout.IsExpired():
            for z in range(nLED):
                pixel = colorsys.hsv_to_rgb((z + translate) * p, 1, 1)
                drawer.SetColor(z, ColorRGB(pixel[0] * intensity, pixel[1] * intensity, pixel[2] * intensity))
            drawer.Show()

            if translate==nLED * 30:
                translateIncr = -1
            elif translate == 0:
                translateIncr = 1

            translate = translate + translateIncr
            #time.sleep(0.03)

class BeadsEffect(PixelEffect):
    def Play(self, drawer, timeout):
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

            if intens>drawer.IntensityMax or intens<1:
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

class RandomBlinksEffect(PixelEffect):
    def Play(self, drawer, timeout):
        nLED = drawer.nLED
        blinks = []  
        maxLeds = 10  
        intensity = drawer.IntensityMax

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

class ColorBounceEffect(PixelEffect):                         #-m5-BOUNCE COLOR (SINGLE LED)
    def Play(self, drawer, timeout):    
        bounceDirection = 0
        idex = 0
        intensity = drawer.IntensityMax

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

class FullFadeEffect(PixelEffect):
    def Play(self, drawer, timeout):
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

class WavesEffect(PixelEffect):
    def __init__(self, steps, cycles):
        self.Steps = steps
        self.Cycles = cycles

    def Play(self, drawer, timeout):
        currentStep = 0
        currentCycle = 0
        intensityMin = drawer.IntensityMin
        intensityMax = drawer.IntensityMax
        targetColor = getRandomColor(2,intensityMin,intensityMax)
        transitionCycle = -1
        cycles = self.Cycles

        while not timeout.IsExpired():
            if currentCycle >= self.Cycles:
                if currentCycle == self.Cycles:
                    targetTransitionColor = getRandomColor(2,intensityMin,intensityMax)

                transitionCycle = currentCycle - self.Cycles
                
                if transitionCycle == drawer.nLED:
                    transitionCycle = -1
                    targetColor = targetTransitionColor                
                    currentCycle = 0

            currentCycle = currentCycle + 1
            currentStep = currentStep + 1

            for z in range(0, drawer.nLED -1):
                m = abs(math.sin((z + currentStep) / self.Steps))
                
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

class RainbowWavesEffect(PixelEffect):
    def __init__(self, steps, cycles):
        self.Steps = steps
        self.Cycles = cycles

    def Play(self, drawer, timeout):
        currentStep = 0
        currentCycle = 0
        #intensityMin = drawer.IntensityMin
        intensityMax = drawer.IntensityMax
        #targetColor = getRandomColor(2,intensityMin,intensityMax)
        transitionCycle = -1
        #cycles = self.Cycles

        #translate = 0
        #translateIncr = 1
        p = 1.0 / (drawer.nLED * 5)
        
        while not timeout.IsExpired():
            if currentCycle >= self.Cycles:
                transitionCycle = transitionCycle + 1                
                if currentCycle - self.Cycles == drawer.nLED:
                    currentCycle = 0

            currentCycle = currentCycle + 1
            currentStep = currentStep + 1

            for z in range(0, drawer.nLED -1):
                pixel = colorsys.hsv_to_rgb((z + transitionCycle) * p, 1, 1)

                m = abs(math.sin((z + currentStep) / self.Steps))                
                c = ColorRGB(pixel[0] * intensityMax, pixel[1] * intensityMax, pixel[2] * intensityMax)
                mC = c.multiply(m, True)
                drawer.SetColor(z, mC)
                
            drawer.Show()

class RandomReplacementEffect(PixelEffect):
    def Play(self, drawer, timeout):
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

class SwitchColorsEffect(PixelEffect):
    def Play(self, drawer, timeout):
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

class DropsEffect(PixelEffect):
    def Play(self, drawer, timeout):
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

class FillEffect(PixelEffect):
    def Play(self, drawer, timeout):
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

class Thread(PixelEffect):
    def Play(self, drawer, timeout):    
        for lastNumber in range(drawer.nLED - 1, 0, -1):
            ledColor = getRandomColor(2,3,20)
            if timeout.IsExpired:
                return
            for ledNumber in range(1,lastNumber):
                drawer.SetColor(ledNumber,ledColor)
                drawer.SetColor(ledNumber-1,ColorRGB())
                drawer.Show()

class Thread2(PixelEffect):
    def Play(self, drawer, timeout):
        nCL=int(drawer.nLED/2)
        for lastNumber in range(1,nCL- 1):
            ledColor = getRandomColor(2,3,20)
            if timeout.IsExpired:
                return
            for ledNumber in range(1,nCL - lastNumber):            
                drawer.SetColor(nCL-ledNumber,ledColor)
                drawer.SetColor(nCL-ledNumber+1,ColorRGB())
                drawer.SetColor(nCL+ledNumber,ledColor)
                drawer.SetColor(nCL+ledNumber-1,ColorRGB())
                drawer.Show()
            
            
class Skittles(PixelEffect):
    def Play(self, drawer, timeout):    
        while not timeout.IsExpired():
            for z in range(0,drawer.nLED-1):
                drawer.SetColor(z, getRandomColor(2,3,20))
            drawer.Show()
            time.sleep(3)

class ColorRunaway(PixelEffect):
    def Play(self, drawer, timeout):    
        while not timeout.IsExpired():
            ps = random.randint(0, drawer.nLED-1)
            pl = pr = ps
            color = getRandomColor(2, drawer.IntensityMin, drawer.IntensityMax)
            speed = 0
            drawer.SetColor(ps, color)
            drawer.Show()
            while True:
                speed += 1
                pl -= speed
                pr += speed

                if pl < 0 or pr > drawer.nLED - 1:
                    #print ("Brake")
                    break

                for p in range(pl,pr):
                    drawer.SetColor(p,color)
                
                drawer.Show()
                time.sleep(0.1)



                #print ("pl: " + str(pl) + ", pr: " + str(pr))
                #time.sleep(1)




