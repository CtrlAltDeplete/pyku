import HSV
import Polygon
import Palette
import RGB
import Watercolor
import Wander

from Functions import *
from os import listdir
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from random import randint
from random import seed


def draw_text(img, text):
    font_name = "fonts/" + choice([filename for filename in listdir("fonts")])
    font_size = 10
    font = ImageFont.truetype(font_name, font_size)
    text_width, text_height = font.getsize(text)
    while text_width < img.width * 4 / 5 and text_height < img.height * 4 / 5:
        font_size += 1
        font = ImageFont.truetype(font_name, font_size)
        text_width, text_height = font.getsize(text)
    draw = ImageDraw.Draw(img, "RGB")
    x = randint(0, img.width - text_width)
    y = randint(0, img.height - text_height)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            draw.text((x + dx, y + dy), text, font=font, fill="white")
    draw.text((x, y), text, font=font, fill="black")


def create_RGB(name):
    RGB.save_RGB(1024, 512, name)


def create_HSV(name):
    HSV.save_HSV(1024, 512, name)


def create_palette(name):
    Palette.save_palette(1024, 512, name, random() > 0.5)


def create_watercolor(name):
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


def create_wander(name):
    Wander.save_wander(name, 1024, 512, 150)


def create_polygon(name):
    Polygon.save_polygon_png(1024, 512, name)


def create_attachment(text, name="test", s=None):
    if s is not None:
        seed(s)
    choice([create_RGB, create_HSV, create_palette, create_palette, create_polygon, create_watercolor, create_wander])(name)
    final_image = Image.open("{}.png".format(name))
    draw_text(final_image, text)
    final_image.save("{}.png".format(name), "PNG")


if __name__ == '__main__':
    create_attachment("This is a poorly\nwritten haiku as a test\nto check if this works.")
