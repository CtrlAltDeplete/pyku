import multiprocessing

from Functions import *
from PIL import Image as PILImage
from random import randint


class RGBImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.red = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.green = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.blue = {
            "tree": FunctionNode(0.6),
            "values": [],
            "shift": randint(0, 255),
            "range": randint(1, 256)
        }
        self.generate()

    def generate(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        jobs = []
        for func in self._generate_reds, self._generate_greens, self._generate_blues:
            p = multiprocessing.Process(target=func, args=(return_dict,))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()

        self.red["values"] = return_dict["red"]
        self.green["values"] = return_dict["green"]
        self.blue["values"] = return_dict["blue"]

    def _generate_reds(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = map_to(y, 0, self.height, -1, 1)
            for x in range(self.width):
                adjusted_x = map_to(x, 0, self.width, -1, 1)
                values.append(self.red["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["red"] = values
        else:
            self.red["values"] = values

    def _generate_greens(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = map_to(y, 0, self.height, -1, 1)
            for x in range(self.width):
                adjusted_x = map_to(x, 0, self.width, -1, 1)
                values.append(self.green["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["green"] = values
        else:
            self.green["values"] = values

    def _generate_blues(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = map_to(y, 0, self.height, -1, 1)
            for x in range(self.width):
                adjusted_x = map_to(x, 0, self.width, -1, 1)
                values.append(self.blue["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["blue"] = values
        else:
            self.blue["values"] = values

    def _new_red(self, complexity=0.6):
        self.red["tree"] = FunctionNode(complexity)
        self._generate_reds()

    def _new_green(self, complexity=0.6):
        self.green["tree"] = FunctionNode(complexity)
        self._generate_greens()

    def _new_blue(self, complexity=0.6):
        self.blue["tree"] = FunctionNode(complexity)
        self._generate_blues()

    def new(self, complexity=(0.6, 0.6, 0.6)):
        self.red["tree"] = FunctionNode(complexity[0])
        self.green["tree"] = FunctionNode(complexity[1])
        self.blue["tree"] = FunctionNode(complexity[2])
        self.generate()


def generate_band(width, height, visible, head, shift, stretch):
    if visible:
        band = PILImage.new("L", (width, height))
        data = []
        for y in range(height):
            adjusted_y = 2 * y / height
            for x in range(width):
                adjusted_x = 2 * x / width
                data.append(((head.eval(adjusted_x, adjusted_y) / 2 + 0.5) * stretch + shift) % 256)
        band.putdata(data)
    else:
        band = PILImage.new("L", (width, height), color=shift)
    return band


def save_RGB(width, height, name):
    rgb_image = RGBImage(width, height)
    color = rgb_image.red, rgb_image.green, rgb_image.blue
    bands = [generate_band(width, height, True, color[i]["tree"], color[i]["shift"], color[i]["range"]) for i in range(3)]

    final_image = PILImage.merge("RGB", bands)
    final_image.save(name + ".png", "PNG")
