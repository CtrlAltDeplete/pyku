from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from random import randint
from Functions import *
from random import seed
import math


font_params = {
    '256BYTES.ttf': 50,
    'Courier New.ttf': 34,
    'data-latin.ttf': 40,
    'Debby.ttf': 66,
    'mexcellent 3d.ttf': 44,
    'Pokemon_GB.ttf': 20,
    'heav.ttf': 42,
    'KOMIKAB_.ttf': 40,
    'federalescort.ttf': 28,
    'HAMMERHEAD.ttf': 35,
    'mytype.ttf': 33,
    'orange juice 2.0.ttf': 50,
    'MotionPicture.ttf': 84,
    'airstrike.ttf': 36,
    'SnackerComic.ttf': 60
}


def hexToDec(hex):
    hexes = "0123456789abcdef"
    return hexes.index(hex[0]) * 16 + hexes.index(hex[1]),\
           hexes.index(hex[2]) * 16 + hexes.index(hex[3]),\
           hexes.index(hex[4]) * 16 + hexes.index(hex[5])


palettes = []
with open("palettes.txt", 'r') as f:
    data = f.readlines()
for p in data:
    datum = p[19:-1].split('-')
    palettes.append(tuple(hexToDec(c) for c in datum))


class PaletteImage:
    def __init__(self, width, height, colorTree, colors):
        self.width = width
        self.height = height
        self.colorTree = colorTree
        self.colors = colors
        self.canvas = Image.new("RGB", (width, height))
        data = {}
        cValues = []
        for x in range(width):
            newX = (x - (width / 2)) / width * 2
            data[x] = {}
            for y in range(height):
                newY = (y - (height / 2)) / height * 2
                c = self.colorTree.eval(newX, newY)
                data[x][y] = c
                cValues.append(c)
        cValues.sort()
        breaks = []
        for i in range(1, len(colors)):
            breaks.append(cValues[int(i * len(cValues) / len(colors))])
        breaks.reverse()
        for x in data.keys():
            for y in data[x].keys():
                cIndex = len(colors) - 1
                for b in breaks:
                    if data[x][y] < b:
                        cIndex = breaks.index(b)
                self.canvas.putpixel((x, y), colors[cIndex])

    def save(self, name):
        self.canvas.save("{}".format(name), "PNG")


class RGB:
    def __init__(self, width, height, red, green, blue):
        self.width = width
        self.height = height
        self.red = red
        self.green = green
        self.blue = blue
        self.canvas = Image.new("RGB", (width, height))
        for x in range(width):
            for y in range(height):
                newX = (x - (width / 2)) / width * 2
                newY = (y - (height / 2)) / height * 2
                r = (self.red.eval(newX, newY) + 1) * 127.5
                g = (self.green.eval(newX, newY) + 1) * 127.5
                b = (self.blue.eval(newX, newY) + 1) * 127.5
                self.canvas.putpixel((x, y), (int(r), int(g), int(b)))

    def save(self, name):
        self.canvas.save("{}".format(name), "PNG")


class HSL:
    def __init__(self, width, height, red, green, blue):
        self.width = width
        self.height = height
        self.red = red
        self.green = green
        self.blue = blue
        self.canvas = Image.new("RGB", (width, height))
        self.dh = randint(0, 360)
        self.ch = randint(15, 60)
        for x in range(width):
            for y in range(height):
                newX = (x - (width / 2)) / width * 2
                newY = (y - (height / 2)) / height * 2
                h = ((self.red.eval(newX, newY) + 1) * self.ch + self.dh) % 360
                s = (self.green.eval(newX, newY) + 1) * .5
                l = (self.blue.eval(newX, newY) + 1) * .5
                c = (1 - abs(2 * l - 1)) * s
                x1 = c * (1 - abs((h / 60) % 2 - 1))
                m = l - c / 2
                if 0 <= h < 60:
                    r, g, b = c, x1, 0
                elif 60 <= h < 120:
                    r, g, b = x1, c, 0
                elif 120 <= h < 180:
                    r, g, b = 0, c, x1
                elif 180 <= h < 240:
                    r, g, b = 0, x1, c
                elif 240 <= h < 300:
                    r, g, b = x1, 0, c
                else:
                    r, g, b = c, 0, x1
                self.canvas.putpixel((x, y), (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)))

    def save(self, name):
        self.canvas.save("{}".format(name), "png")


class HSV:
    def __init__(self, width, height, red, green, blue):
        self.width = width
        self.height = height
        self.red = red
        self.green = green
        self.blue = blue
        self.canvas = Image.new("RGB", (width, height))
        self.dh = randint(0, 360)
        self.ch = randint(15, 60)
        for x in range(width):
            for y in range(height):
                newX = (x - (width / 2)) / width * 2
                newY = (y - (height / 2)) / height * 2
                h = ((self.red.eval(newX, newY) + 1) * self.ch + self.dh) % 360
                s = (self.green.eval(newX, newY) + 1) * .5
                v = (self.blue.eval(newX, newY) + 1) * .5
                c = v * s
                x1 = c * (1 - abs((h / 60) % 2 - 1))
                m = v - c
                if 0 <= h < 60:
                    r, g, b = c, x1, 0
                elif 60 <= h < 120:
                    r, g, b = x1, c, 0
                elif 120 <= h < 180:
                    r, g, b = 0, c, x1
                elif 180 <= h < 240:
                    r, g, b = 0, x1, c
                elif 240 <= h < 300:
                    r, g, b = x1, 0, c
                else:
                    r, g, b = c, 0, x1
                self.canvas.putpixel((x, y), (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)))

    def save(self, name):
        self.canvas.save("{}".format(name), "png")


class WaterColor:
    def __init__(self, size):
        self.width, self.height = size
        self.canvas = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.canvas, "RGBA")

    def paintStrokes(self, strokeCount, brushMin, brushMax, thickMin, thickMax, palette):
        c = 0
        for i in range(strokeCount):
            c += 1
            c %= len(palette)
            # Create and Draw Stroke
            points = []
            numPoints = randint(3, 10)
            for j in range(numPoints):
                x = randint(-self.width // 2, self.width * 3 // 2)
                y = randint(-self.height // 2, self.height * 3 // 2)
                points.append((x, y))
            size = randint(brushMin, brushMax)
            for j in range(randint(thickMin, thickMax)):
                newPoints = []
                dx, dy = randint(-5, 5), randint(-5, 5)
                for p in points:
                    newPoints.append((p[0] + dx, p[1] + dy))
                bcurve = self.bcurve(newPoints, steps=3 * numPoints)
                dSize = randint(-brushMin // 4, brushMin // 4)
                stroke = self.createStroke(bcurve, size + dSize)
                poly = stroke
                for k in range(randint(brushMin // 8, brushMin // 4)):
                    poly = self.deformPolygon(poly)
                self.draw.polygon(poly, fill=(palette[c][0], palette[c][1], palette[c][2], randint(3, 15)))

    def paintBlobs(self, blobCount, brushMin, brushMax, thickMin, thickMax, palette):
        c = 0
        for i in range(blobCount):
            c += 1
            c %= len(palette)
            # Create and Draw Blob
            x = randint(-brushMax, self.width + brushMax)
            y = randint(-brushMax, self.height + brushMax)
            size = randint(brushMin, brushMax)
            for j in range(randint(thickMin, thickMax)):
                x += randint(-5, 5)
                y += randint(-5, 5)
                size += randint(-brushMin // 4, brushMin // 4)
                blob = self.createBlob((x, y), size)
                poly = blob
                for k in range(randint(brushMin // 4, brushMin // 2)):
                    poly = self.deformPolygon(poly)
                self.draw.polygon(poly, fill=(palette[c][0], palette[c][1], palette[c][2], randint(3, 15)))

    def bcurve(self, points, steps=12):
        newPoints = []
        for i in range(steps):
            t = i / (steps - 1)
            x = 0
            y = 0
            for n in range(len(points)):
                coef1 = math.factorial(len(points) - 1) / (math.factorial(len(points) - 1 - n) * math.factorial(n))
                coef2 = (1 - t) ** (len(points) - 1 - n)
                coef3 = t ** n
                x += coef1 * coef2 * coef3 * points[n][0]
                y += coef1 * coef2 * coef3 * points[n][1]
            newPoints.append((x, y))
        return newPoints

    def createStroke(self, points, size):
        strokePoints = []
        # Draw the rounded beginning, starting with the upper perp
        angle = self.calcPerp(points[0], points[1])
        for i in range(4):
            x = points[0][0] + size * math.cos(angle)
            y = points[0][1] + size * math.sin(angle)
            strokePoints.append((x, y))
            angle += math.pi / 3
        # Draw the lower perp for each mid point
        for i in range(1, len(points) - 1):
            angle = self.calcPerp(points[i - 1], points[i + 1], False)
            x = points[i][0] + size * math.cos(angle)
            y = points[i][1] + size * math.sin(angle)
            strokePoints.append((x, y))
        # Draw the rounded end, starting with the lower perp
        angle = self.calcPerp(points[-2], points[-1], False)
        for i in range(4):
            x = points[-1][0] + size * math.cos(angle)
            y = points[-1][1] + size * math.sin(angle)
            strokePoints.append((x, y))
            angle += math.pi / 3
        # Draw the upper perp for each mid point
        for i in range(1, len(points) - 1):
            angle = self.calcPerp(points[len(points) - i - 2], points[len(points) - i])
            x = points[len(points) - 1 - i][0] + size * math.cos(angle)
            y = points[len(points) - 1 - i][1] + size * math.sin(angle)
            strokePoints.append((x, y))
        return strokePoints

    def createBlob(self, point, size):
        blobPoints = []
        angle = randint(0, 359) / 360 * 2 * math.pi
        for i in range(6):
            blobPoints.append((point[0] + math.cos(angle) * size, point[1] + math.sin(angle) * size))
            angle += math.pi / 3
        return blobPoints

    def deformPolygon(self, polygon):
        def randPoint(p1, p2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            try:
                x = dx / abs(dx) * randint(0, int(abs(dx)))
            except ZeroDivisionError:
                x = 0
            try:
                y = dy / abs(dy) * randint(0, int(abs(dy)))
            except ZeroDivisionError:
                y = 0
            return p1[0] + x, p1[1] + y

        newPoly = []
        for i in range(len(polygon)):
            p1 = polygon[i]
            if len(polygon) - 1 == i:
                p2 = polygon[0]
                newPoly.append(p1)
            else:
                p2 = polygon[i + 1]
            newPoly.append(randPoint(p1, p2))
            newPoly.append(p2)
        return newPoly

    def calcAngle(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        quad = 1
        if dx < 0:
            if dy < 0:
                quad = 3
            else:
                quad = 2
        else:
            if dy < 0:
                quad = 4
        try:
            angle = math.atan(dy / dx)
            if quad == 2:
                angle += math.pi
            elif quad == 3:
                angle = math.pi + angle
        except ZeroDivisionError:
            if dy > 0:
                angle = math.pi / 2
            else:
                angle = 3 * math.pi / 2
        while angle < 0 or angle >= 2 * math.pi:
            angle += (math.pi * 2)
            angle %= (math.pi * 2)
        return angle

    def calcPerp(self, p1, p2, upper=True):
        if upper:
            angle = self.calcAngle(p1, p2) + math.pi / 2
        else:
            angle = self.calcAngle(p1, p2) - math.pi / 2
        while angle < 0 or angle >= 2 * math.pi:
            angle += (math.pi * 2)
            angle %= (math.pi * 2)
        return angle

    def save(self, name):
        self.canvas.save("{}".format(name), "png")


def createText(width, height, words, font, size):
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/{}".format(font), size)
    draw.text((20, 20), words, (255, 255, 255), font=font)
    effectedPixels = []
    minX = width
    maxX = 0
    minY = height
    maxY = 0
    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) != (0, 0, 0):
                effectedPixels.append([x, y])
                minX = min(minX, x)
                minY = min(minY, y)
                maxX = max(maxX, x)
                maxY = max(maxY, y)
    for i in range(len(effectedPixels)):
        effectedPixels[i] = [effectedPixels[i][0] - minX, effectedPixels[i][1] - minY]
    width = maxX - minX
    height = maxY - minY
    dx = randint(0, img.width - width - 1)
    dy = randint(0, img.height - height - 1)
    return effectedPixels, dx, dy


def drawText(effectedPixels, dx, dy, img):
    for p in effectedPixels:
        for x in range(-2, 3):
            for y in range(-2, 3):
                try:
                    img.putpixel((p[0] + dx + x, p[1] + dy + y), (0, 0, 0))
                except IndexError:
                    pass
    for p in effectedPixels:
        img.putpixel((p[0] + dx, p[1] + dy), (255, 255, 255))


def createRGB():
    rHead = FunctionNode(randint(80, 90) / 100)
    gHead = FunctionNode(randint(80, 90) / 100)
    bHead = FunctionNode(randint(80, 90) / 100)
    finalImage = RGB(1024, 512, rHead, gHead, bHead)
    return finalImage


def createHSL():
    hHead = FunctionNode(randint(80, 90) / 100)
    sHead = FunctionNode(randint(50, 70) / 100)
    lHead = FunctionNode(randint(50, 70) / 100)
    finalImage = HSL(1024, 512, hHead, sHead, lHead)
    return finalImage


def createHSV():
    hHead = FunctionNode(randint(80, 90) / 100)
    sHead = FunctionNode(randint(50, 70) / 100)
    vHead = FunctionNode(randint(50, 70) / 100)
    finalImage = HSV(1024, 512, hHead, sHead, vHead)
    return finalImage


def createPaletteBased():
    cHead = FunctionNode(randint(80, 90) / 100)
    finalImage = PaletteImage(1024, 512, cHead, choice(palettes))
    return finalImage


def createWaterColor():
    finalImage = WaterColor((1024, 512))
    palette = choice(palettes)
    finalImage.paintBlobs(randint(500, 600), 10, 90, 5, 10, palette)
    finalImage.paintStrokes(randint(20, 40), 30, 60, 3, 6, palette)
    return finalImage


def createAttachment(name, text, s=None):
    if s is not None:
        seed(s)
    finalImage = choice([createRGB, createHSL, createHSV, createPaletteBased, createWaterColor])()
    font = choice(list(font_params.keys()))
    fontSize = randint(font_params[font], int(font_params[font] * 1.5))
    effectedPixels, dx, dy = createText(1024, 512, text, font, fontSize)
    drawText(effectedPixels, dx, dy, finalImage.canvas)
    finalImage.save("{}.png".format(name))
    return "{}.png".format(name)


if __name__ == '__main__':
    createAttachment("test", "This is a poorly\nwritten haiku as a test\nto check if this works.")
    # font = 'mytype.ttf'
    # fontSize = font_params[font]
    # createText(512, 256, "This is a poorly\nwritten haiku as a test\nto check if this works.", font, fontSize)
