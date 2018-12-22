import math

from Functions import *
from PIL import Image as PILImage
from PIL import ImageDraw


class FieldImage:
    class Field:
        def __init__(self, width, height, node_step, force):
            tree = FunctionNode(0.99)
            self.nodes = {}
            self.node_step = node_step
            self.force = force
            self.width, self.height = width, height
            for y in range(-height // (8 * self.node_step) * self.node_step, 9 * height // 8, self.node_step):
                adjusted_y = map_to(y, -height // (8 * self.node_step) * self.node_step, 9 * height // 8, -1, 1)
                for x in range(-width // (8 * self.node_step) * self.node_step, 9 * width // 8, self.node_step):
                    adjusted_x = map_to(x, -width // (8 * self.node_step) * self.node_step, 9 * width // 8, -1, 1)
                    self.nodes[(x, y)] = map_to(tree.eval(adjusted_x, adjusted_y), -1, 1, 0, 2 * math.pi)

        def _determine_effectors(self, pos):
            x, y = pos
            x_range = (x // self.node_step * self.node_step, x // self.node_step * self.node_step + self.node_step)
            y_range = (y // self.node_step * self.node_step, y // self.node_step * self.node_step + self.node_step)
            effectors = []
            for y in y_range:
                for x in x_range:
                    if -self.height // 8 <= y < 9 * self.height // 8 and -self.width // 8 <= x < 9 * self.width // 8:
                        effectors.append((x, y))
            return effectors

        def _calculate_force(self, pos, effector):
            distance = (pos[0] - effector[0]) ** 2 + (pos[1] - effector[1]) ** 2
            magnitude = map_to(distance, 0, self.node_step ** 2 * 2, self.force * 2, self.force / 2)
            x_force = magnitude * math.cos(self.nodes[effector])
            y_force = magnitude * math.sin(self.nodes[effector])
            return x_force, y_force

        def calculate_sigma_force(self, pos):
            effectors = self._determine_effectors(pos)
            force = [0, 0]
            for e in effectors:
                xf, yf = self._calculate_force(pos, e)
                force[0] += xf
                force[1] += yf
            return force

    def __init__(self, width, height, name, time_step, force):
        self.field = self.Field(width, height, 5, force)
        self.color_tree = (FunctionNode(0.8), FunctionNode(0.8), FunctionNode(0.8))
        self.img = PILImage.new("RGB", (width, height), color=(255, 255, 255))
        self.time_step = time_step
        self.draw = ImageDraw.ImageDraw(self.img, "RGBA")
        self.width = width
        self.height = height
        self.name = name
        self.pens = []

    def _update_pen_force(self, pen):
        t = self.time_step
        pen["force"] = self.field.calculate_sigma_force(pen["position"])
        pen["acceleration"] = (
            pen["force"][0] / pen["mass"],
            pen["force"][1] / pen["mass"]
        )

    def _update_pen_vel(self, pen):
        t = self.time_step
        pen["velocity"] = (
            t * pen["acceleration"][0] + pen["velocity"][0],
            t * pen["acceleration"][1] + pen["velocity"][1]
        )

    def _update_pen_pos(self, pen):
        t = self.time_step
        pen["position"] = (
            pen["position"][0] + pen["velocity"][0] * t + 0.5 * pen["force"][0] * t * t,
            pen["position"][1] + pen["velocity"][1] * t + 0.5 * pen["force"][1] * t * t
        )

    def update_pen(self, pen):
        old_pos = pen["position"]
        self._update_pen_force(pen)
        self._update_pen_vel(pen)
        self._update_pen_pos(pen)
        self.draw.line([old_pos, pen["position"]], fill=pen["color"], width=4)
        self.draw.line([old_pos, pen["position"]], fill=pen["color"], width=8)
        self.draw.line([old_pos, pen["position"]], fill=pen["color"], width=12)
        if -self.width // 8 <= pen["position"][0] <= 9 * self.width // 8 and -self.height // 8 <= pen["position"][1] <= 9 * self.height // 8:
            return True
        return False

    def update_all_pens(self):
        to_remove = []
        for pen in self.pens:
            keep = self.update_pen(pen)
            if not keep:
                to_remove.append(pen)
        for pen in to_remove:
            self.pens.remove(pen)

    def create_png(self, time):
        for y in range(-self.height // 8, 9 * self.height // 8, 5):
            for x in range(-self.width // 8, 9 * self.width // 8, 5):
                self.new_pen((x, y))
        for i in range(time):
            self.update_all_pens()
        self.img.save("{}.png".format(self.name), "PNG")

    def new_pen(self, pos):
        self.pens.append(
            {
                "position": pos,
                "force": (0, 0),
                "acceleration": (0, 0),
                "velocity": (0, 0),
                "mass": 10,
                "color": (
                    int(map_to(self.color_tree[0].eval(pos[0], pos[1]), -1, 1, 0, 255)),
                    int(map_to(self.color_tree[1].eval(pos[0], pos[1]), -1, 1, 0, 255)),
                    int(map_to(self.color_tree[2].eval(pos[0], pos[1]), -1, 1, 0, 255)),
                    2
                )
            }
        )


def save_wander(name, width, height, time):
    field_img = FieldImage(width, height, name, 1, 1)
    field_img.create_png(time)
