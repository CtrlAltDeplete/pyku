from Functions import *
from PIL import Image as PILImage
from random import randint


class PaletteImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.palette = {
            "tree": FunctionNode(0.8),
            "values": [],
            "breakpoints": {},
            "domain": []
        }
        self.generate()
        self.generate_breakpoints()

    def generate(self):
        values = []
        for y in range(self.height):
            adjusted_y = map_to(y, 0, self.height, -1, 1)
            for x in range(self.width):
                adjusted_x = map_to(x, 0, self.width, -1, 1)
                values.append(self.palette["tree"].eval(adjusted_x, adjusted_y))
        self.palette["values"] = values
        self.palette["domain"] = [min(values), max(values)]

    def generate_breakpoints(self):
        sorted_values = self.palette["values"].copy()
        sorted_values.sort()

        for i in range(0, 101):
            self.palette["breakpoints"][i] = sorted_values[int((len(sorted_values) - 1) * i / 100)]

    def new(self, complexity=0.8):
        self.palette["tree"] = FunctionNode(complexity)
        self.generate()
        self.generate_breakpoints()


def save_palette(width, height, name, fuzzy):
    palette_image = PaletteImage(width, height)
    breakpoints = [20, 40, 60, 80]
    data = []
    if fuzzy:
        for v in palette_image.palette["values"]:
            if v < palette_image.palette["breakpoints"][breakpoints[0] + randint(-5, 5)]:
                data.append(0)
            elif v < palette_image.palette["breakpoints"][breakpoints[1] + randint(-5, 5)]:
                data.append(1)
            elif v < palette_image.palette["breakpoints"][breakpoints[2] + randint(-5, 5)]:
                data.append(2)
            elif v < palette_image.palette["breakpoints"][breakpoints[3] + randint(-5, 5)]:
                data.append(3)
            else:
                data.append(4)
    else:
        for v in palette_image.palette["values"]:
            if v < palette_image.palette["breakpoints"][breakpoints[0]]:
                data.append(0)
            elif v < palette_image.palette["breakpoints"][breakpoints[1]]:
                data.append(1)
            elif v < palette_image.palette["breakpoints"][breakpoints[2]]:
                data.append(2)
            elif v < palette_image.palette["breakpoints"][breakpoints[3]]:
                data.append(3)
            else:
                data.append(4)
    colors = [(randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255)),
              (randint(0, 255), randint(0, 255), randint(0, 255))]
    new_data = [colors[i] for i in data]
    final_image = PILImage.new("RGB", (width, height))
    final_image.putdata(new_data)
    final_image.save(name + ".png", "PNG")
