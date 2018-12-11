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


font_params = [
    '256BYTES.ttf',
    'Courier New.ttf',
    'data-latin.ttf',
    'Debby.ttf',
    'mexcellent 3d.ttf',
    'Pokemon_GB.ttf',
    'heav.ttf',
    'KOMIKAB_.ttf',
    'federalescort.ttf',
    'HAMMERHEAD.ttf',
    'mytype.ttf',
    'orange juice 2.0.ttf',
    'MotionPicture.ttf',
    'airstrike.ttf',
    'SnackerComic.ttf'
]


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


def drawText(img, text):
    font_name = "fonts/" + choice(font_params)
    font_size = 10
    font = ImageFont.truetype(font_name, font_size)
    text_width, text_height = font.getsize(text)
    while text_width < img.width * 3 // 4 and text_height < img.height * 3 // 4:
        font_size += 5
        font = ImageFont.truetype(font_name, font_size)
        text_width, text_height = font.getsize(text)
    draw = ImageDraw.Draw(img, "RGB")
    x = randint(0, img.width - text_width)
    y = randint(0, img.height - text_height)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            draw.text((x + dx, y + dy), text, font=font, fill="white")
    draw.text((x, y), text, font=font, fill="black")


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
    drawText(finalImage, text)
    finalImage.save("{}.png".format(name), "PNG")


if __name__ == '__main__':
    createAttachment("This is a poorly\nwritten haiku as a test\nto check if this works.")
    # font = 'mytype.ttf'
    # fontSize = font_params[font]
    # createText(512, 256, "This is a poorly\nwritten haiku as a test\nto check if this works.", font, fontSize)
