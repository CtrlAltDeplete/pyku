import math
import multiprocessing

from Functions import *
from PIL import Image as PILImage
from PIL import ImageDraw
from random import randint


class PolygonImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.polygon = {
            "sides": 6,
            "angles": [math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180],
            "distances": [randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100,
                          randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100]
        }
        self.polygon["angles"].sort()
        self.hue = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.sat = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.val = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.opac = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.rot = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 359),
            "range": randint(1, 360)
        }
        self.size = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(5, 50),
            "range": randint(5, 50)
        }
        self.step_size = 5
        self.generate()

    def generate(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        jobs = []
        for func in (self._generate_hues, self._generate_sats, self._generate_vals, self._generate_opacs,
                     self._generate_rots, self._generate_sizes):
            p = multiprocessing.Process(target=func, args=(return_dict,))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()

        self.hue["values"] = return_dict["hue"]
        self.sat["values"] = return_dict["sat"]
        self.val["values"] = return_dict["val"]
        self.opac["values"] = return_dict["opac"]
        self.rot["values"] = return_dict["rot"]
        self.size["values"] = return_dict["size"]

    def new_polygon(self):
        self.polygon = {
            "sides": 6,
            "angles": [math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180,
                       math.pi * randint(0, 359) / 180, math.pi * randint(0, 359) / 180],
            "distances": [randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100,
                          randint(1, 100) / 100, randint(1, 100) / 100, randint(1, 100) / 100]
        }
        self.polygon["angles"].sort()

    def _generate_hues(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.hue["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["hue"] = values
        else:
            self.hue["values"] = values

    def _generate_sats(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.sat["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["sat"] = values
        else:
            self.sat["values"] = values

    def _generate_vals(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.val["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["val"] = values
        else:
            self.val["values"] = values

    def _generate_opacs(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.opac["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["opac"] = values
        else:
            self.opac["values"] = values

    def _generate_rots(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.rot["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["rot"] = values
        else:
            self.rot["values"] = values

    def _generate_sizes(self, return_dict=None):
        values = []
        for y in range(-self.step_size, self.height + self.step_size, self.step_size):
            adjusted_y = 2 * y / self.height
            for x in range(-self.step_size, self.width + self.step_size, self.step_size):
                adjusted_x = 2 * x / self.width
                values.append(self.size["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["size"] = values
        else:
            self.size["values"] = values

    def _new_hue(self, complexity=0.6):
        self.hue["tree"] = FunctionNode(complexity)
        self._generate_hues()

    def _new_sat(self, complexity=0.6):
        self.sat["tree"] = FunctionNode(complexity)
        self._generate_sats()

    def _new_val(self, complexity=0.6):
        self.val["tree"] = FunctionNode(complexity)
        self._generate_vals()

    def _new_opac(self, complexity=0.6):
        self.opac["tree"] = FunctionNode(complexity)
        self._generate_opacs()

    def _new_rot(self, complexity=0.6):
        self.rot["tree"] = FunctionNode(complexity)
        self._generate_rots()

    def _new_size(self, complexity=0.6):
        self.size["tree"] = FunctionNode(complexity)
        self._generate_sizes()

    def new(self, complexity=(0.6, 0.6, 0.6, 0.6, 0.6, 0.6)):
        self.hue["tree"] = FunctionNode(complexity[0])
        self.sat["tree"] = FunctionNode(complexity[1])
        self.val["tree"] = FunctionNode(complexity[2])
        self.opac["tree"] = FunctionNode(complexity[3])
        self.rot["tree"] = FunctionNode(complexity[4])
        self.size["tree"] = FunctionNode(complexity[5])
        self.generate()


def hsv_to_rgb(h, s, v):
    h = 360 * h / 255
    s = s / 255
    v = v / 255
    c = v * s
    x = c * (1 - abs(h / 60 % 2 - 1))
    m = v - c
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


def generate_polygon(poly_image, draw, x, y, i):
    hue = (poly_image.hue["range"] * (poly_image.hue["values"][i] / 2 + 0.5) + poly_image.hue["shift"]) % 255
    sat = (poly_image.sat["range"] * (poly_image.sat["values"][i] / 2 + 0.5) +
           poly_image.sat["shift"]) % 255
    val = (poly_image.val["range"] * (poly_image.val["values"][i] / 2 + 0.5) +
           poly_image.val["shift"]) % 255
    opac = (poly_image.opac["range"] * (poly_image.opac["values"][i] / 2 + 0.5) +
            poly_image.opac["shift"]) % 255
    rot = math.pi * ((poly_image.rot["range"] * (poly_image.rot["values"][i] / 2 + 0.5) +
                      poly_image.rot["shift"]) % 360) / 180
    size = poly_image.size["range"] * (poly_image.size["values"][i] / 2 + 0.5) + \
           poly_image.size["shift"]

    red, green, blue = hsv_to_rgb(hue, sat, val)
    angles = [rot + theta for theta in poly_image.polygon["angles"]]
    distances = [size * dist for dist in poly_image.polygon["distances"]]
    points = []
    for j in range(len(angles)):
        points.append((
            x + distances[j] * math.cos(angles[j]),
            y + distances[j] * math.sin(angles[j])
        ))
    draw.polygon(points, fill=(red, green, blue, int(opac)))


def save_polygon_png(width, height, name):
    poly_image = PolygonImage(width, height)
    pil_image = PILImage.new("RGB", (width, height))
    draw = ImageDraw.Draw(pil_image, "RGBA")

    draw.rectangle([0, 0, width, height], fill=(255, 255, 255))
    i = 0
    for y in range(-poly_image.step_size, height + poly_image.step_size, poly_image.step_size):
        for x in range(-poly_image.step_size, width + poly_image.step_size, poly_image.step_size):
            generate_polygon(poly_image, draw, x, y, i)
            i += 1
    pil_image.save(name + ".png", "PNG")
