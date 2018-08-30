from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from random import randint
from Functions import *


font_params = {
    'Courier New.ttf': {
        'min': 30,
        'max': 40
    },
    'data-latin.ttf': {
        'min': 38,
        'max': 51
    },
    'Debby.ttf': {
        'min': 60,
        'max': 80
    },
    'mexcellent 3d.ttf': {
        'min': 35,
        'max': 47
    },
    'Pokemon_GB.ttf': {
        'min': 18,
        'max': 24
    },
    'Sailor-Scrawl-Black.ttf': {
        'min': 27,
        'max': 36
    }
}


palettes = [
    ((7, 79, 87), (7, 113, 135), (116, 165, 127), (158, 206, 154), (228, 197, 175)),
    ((37, 48, 49), (49, 86, 89), (41, 120, 160), (188, 171, 121), (198, 224, 255)),
    ((237, 212, 178), (208, 169, 143), (77, 36, 61), (202, 194, 181), (236, 220, 201)),
    ((243, 183, 0), (250, 163, 0), (229, 124, 4), (255, 98, 1), (246, 62, 2)),
    ((12, 10, 62), (123, 30, 122), (179, 63, 98), (249, 86, 79), (243, 198, 119)),
    ((58, 64, 90), (249, 222, 201), (153, 178, 221), (233, 175, 163), (104, 80, 68)),
    ((252, 250, 250), (200, 211, 213), (164, 184, 196), (110, 131, 135), (12, 202, 74)),
    ((0, 15, 8), (28, 55, 56), (77, 72, 71), (244, 255, 248), (139, 170, 173))
]


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
                img.putpixel((p[0] + dx + x, p[1] + dy + y), (0, 0, 0))
    for p in effectedPixels:
        img.putpixel((p[0] + dx, p[1] + dy), (255, 255, 255))


def createAttachment(name, text, palette=None):
    if palette is None:
        palette = choice(palettes)
    cHead = FunctionNode(randint(70, 100) / 100)
    finalImage = PaletteImage(1024, 512, cHead, palette)
    font = choice(list(font_params.keys()))
    fontSize = randint(font_params[font]['min'], font_params[font]['max'])
    effectedPixels, dx, dy = createText(1024, 512, text, font, fontSize)
    drawText(effectedPixels, dx, dy, finalImage.canvas)
    finalImage.save("{}.png".format(name))
    return "{}.png".format(name)


if __name__ == '__main__':
    createAttachment("test", "This is a poorly\nwritten haiku as a test\nto check if this works.")
