from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from random import randint
from Functions import *
from random import seed


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


def createText(width, height, words, font, size):
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/{}".format(font), size)
    draw.text((20, 20), words, (255, 255, 255), font=font)
    # img.show()
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


def createAttachment(name, text, palette=None, s=None):
    if s is not None:
        seed(s)
    if palette is None:
        palette = choice(palettes)
    cHead = FunctionNode(randint(70, 100) / 100)
    finalImage = PaletteImage(1024, 512, cHead, palette)
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
