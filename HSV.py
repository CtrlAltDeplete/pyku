import multiprocessing

from Functions import *
from PIL import Image as PILImage
from random import randint


class HSVImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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
        self.generate()

    def generate(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        jobs = []
        for func in self._generate_hues, self._generate_sats, self._generate_vals:
            p = multiprocessing.Process(target=func, args=(return_dict,))
            jobs.append(p)
            p.start()
        for proc in jobs:
            proc.join()

        self.hue["values"] = return_dict["hue"]
        self.sat["values"] = return_dict["sat"]
        self.val["values"] = return_dict["val"]

    def _generate_hues(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.hue["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["hue"] = values
        else:
            self.hue["values"] = values

    def _generate_sats(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.sat["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["sat"] = values
        else:
            self.sat["values"] = values

    def _generate_vals(self, return_dict=None):
        values = []
        for y in range(self.height):
            adjusted_y = 2 * y / self.height
            for x in range(self.width):
                adjusted_x = 2 * x / self.width
                values.append(self.val["tree"].eval(adjusted_x, adjusted_y))
        if return_dict is not None:
            return_dict["val"] = values
        else:
            self.val["values"] = values

    def _new_hue(self, complexity=0.6):
        self.hue["tree"] = FunctionNode(complexity)
        self._generate_hues()

    def _new_sat(self, complexity=0.6):
        self.sat["tree"] = FunctionNode(complexity)
        self._generate_sats()

    def _new_val(self, complexity=0.6):
        self.val["tree"] = FunctionNode(complexity)
        self._generate_vals()

    def new(self, complexity=(0.6, 0.6, 0.6)):
        self.hue["tree"] = FunctionNode(complexity[0])
        self.sat["tree"] = FunctionNode(complexity[1])
        self.val["tree"] = FunctionNode(complexity[2])
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


def save_HSV(width, height, name):
    hsv_image = HSVImage(width, height)
    color = hsv_image.hue, hsv_image.sat, hsv_image.val
    bands = [generate_band(width, height, True, color[i]["tree"], color[i]["shift"], color[i]["range"]) for i in range(3)]

    final_image = PILImage.merge("HSV", bands).convert("RGB")
    final_image.save(name + ".png", "PNG")
