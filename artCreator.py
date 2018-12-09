import HSV
import Polygon
import Palette
import RGB
import Watercolor

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


def createRGB(name):
    RGB.save_RGB(1024, 512, name)


def createHSV(name):
    HSV.save_HSV(1024, 512, name)


def createPalette(name):
    Palette.save_palette(1024, 512, name, random() > 0.5)


def createWatercolor(name):
    blobs = {
        'count': randint(160, 240),
        'size': (35, 75),
        'values': []
    }
    strokes = {
        'count': randint(120, 180),
        'size': (15, 60),
        'values': []
    }
    Watercolor.save_watercolor(name, 1024, 512, blobs, strokes)


def createPolygon(name):
    Polygon.save_polygon_png(1024, 512, name)


def createAttachment(text, name="test", s=None):
    if s is not None:
        seed(s)
    choice([createRGB, createHSV, createPalette, createPolygon, createWatercolor])(name)
    finalImage = Image.open("{}.png".format(name))
    font = choice(list(font_params.keys()))
    fontSize = randint(font_params[font], int(font_params[font] * 1.5))
    effectedPixels, dx, dy = createText(1024, 512, text, font, fontSize)
    drawText(effectedPixels, dx, dy, finalImage)
    finalImage.save("{}.png".format(name), "PNG")


if __name__ == '__main__':
    createAttachment("test", "This is a poorly\nwritten haiku as a test\nto check if this works.")
    # font = 'mytype.ttf'
    # fontSize = font_params[font]
    # createText(512, 256, "This is a poorly\nwritten haiku as a test\nto check if this works.", font, fontSize)
