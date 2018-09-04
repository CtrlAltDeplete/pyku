from random import choice
from random import random
from math import *
from scipy import special


class Function:
    '''This is the parent class for all functions used.'''
    def __init__(self):
        '''When a function is made, it will randomly be assigned a
        delta x and y to make sure everything is not centered.
        Additionally, the input of the function will be [-1, 1],
        and the output of the function needs to be [-1, 1].'''
        self.dx = random() * (-1) ** choice([1, 2]) / 4
        self.dy = random() * (-1) ** choice([1, 2]) / 4
        self.zmin = self.eval(1, 1, False)
        self.zmax = self.zmin
        # To constrict output between -1 and 1, we calclate the max
        # And min output with inputs between -1 and 1, and manipulate
        # The output accordingly.
        for ix in range(-100, 100):
            for iy in range(-100, 100):
                z = self.eval(ix / 100, iy / 100, False)
                self.zmin = min(self.zmin, z)
                self.zmax = max(self.zmax, z)

    def eval(self, x, y, normalized=True):
        return

    def __str__(self):
        pass


class X(Function):
    def __init__(self):
        pass

    def eval(self, x, y, normalized=True):
        return x

    def __str__(self):
        return "x"


class Y(Function):
    def __init__(self):
        pass

    def eval(self, x, y, normalized=True):
        return y

    def __str__(self):
        return "y"


class InverseX(Function):
    def eval(self, x, y, normalized=True):
        if x < 0:
            return abs(x)
        else:
            return -1 * abs(x)

    def __str__(self):
        return "InverseX"


class InverseY(Function):
    def eval(self, x, y, normalized=True):
        if y < 0:
            return abs(y)
        else:
            return -1 * abs(y)

    def __str__(self):
        return "InverseY"


class Ripple(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = newX * newY ** 3 - newY * newX ** 3
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Ripple"


class Sinkhole(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = (newX ** 2 + 3 * newY ** 2) * e ** (-newX ** 2 - newY ** 2)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Sinkhole"


class Pulse(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = -newX * newY * e ** (-newX ** 2 - newY ** 2)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Pulse"


class Hill(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = cos(abs(newX) + abs(newY))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Hill"


class Sinkhole2(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = cos(abs(newX) + abs(newY)) * (abs(newX) + abs(newY))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Sinkhole2"


class Ripple2(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = newX ** 3 - 3 * newX + newY ** 3 - 3 * newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Ripple2"


class Bendy(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = sin(4 * newX * newY)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Bendy"


class Checkered(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = sin(cos(tan(newX))) * sin(cos(tan(newY)))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Checkered"


class Checkered2(Function):
    def eval(self, x, y, normalized=True):
        z = asin(x) + asin(y)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Checkered2"


class Sum(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = newX + newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Sum"


class Product(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = newX * newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Product"


class Mod(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = newX % newY
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Mod"


class Mod2(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = newY % newX
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Mod2"


class Mod3(Function):
    def eval(self, x, y, normalized=True):
        z = x % (self.dx * 10)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Mod3"


class Mod4(Function):
    def eval(self, x, y, normalized=True):
        z = y % self.dy
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Mod4"


class Well(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        z = 1 - 2 / (1 + newX * newX) ** 8
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Well"


class Well2(Function):
    def eval(self, x, y, normalized=True):
        newY = y + self.dy
        z = 1 - 2 / (1 + newY * newY) ** 8
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Well2"


class Tent(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        z = 1 - 2 * abs(newX)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Tent"


class Tent2(Function):
    def eval(self, x, y, normalized=True):
        newY = y + self.dy
        z = 1 - 2 * abs(newY)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "Tent2"


class PolarR(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = sqrt(newX ** 2 + newY ** 2)
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "PolarR"


class PolarTheta(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        try:
            z = atan(newY / newX)
        except ValueError:
            if newX > 0:
                if newY > 0:
                    z = pi / 4
                else:
                    z = 7 * pi / 4
            else:
                if newY > 0:
                    z = 3 * pi / 4
                else:
                    z = 5 * pi / 4
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "PolarTheta"


class GammaLower(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = special.gammainc(abs(newX * 10 + 1), abs(newY * 10))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "GammaLower"


class GammaUpper(Function):
    def eval(self, x, y, normalized=True):
        newX = x + self.dx
        newY = y + self.dy
        z = special.gammainc(abs(newX * 10 + 1), abs(newY * 10))
        if normalized:
            z = max(self.zmin, min(self.zmax, z))
            return (z - self.zmin) / (self.zmax - self.zmin) * 2 - 1
        return z

    def __str__(self):
        return "GammaUpper"


class FunctionNode:
    def __init__(self, prob):
        self.func = choice([Ripple, Sinkhole, Pulse, Hill, Sinkhole2, Ripple2, Bendy, Checkered, Checkered2, Sum,
                            Product, Mod, Mod2, Mod3, Mod4, Well, Well2, Tent, Tent2, InverseX, InverseY, PolarR,
                            PolarTheta, GammaLower, GammaUpper])()
        if random() > prob:
            self.left = X()
        else:
            newProb = prob * prob
            self.left = FunctionNode(newProb)
        if random() > prob:
            self.right = Y()
        else:
            newProb = prob * prob
            self.right = FunctionNode(newProb)

    def eval(self, x, y):
        newX = self.left.eval(x, y)
        newY = self.right.eval(x, y)
        return self.func.eval(newX, newY)


def _createTree(root):
    tree = [str(root.func)]
    queue = [root.left, root.right]

    def checkQueue(q):
        tally = 0
        for x in q:
            if x is None:
                tally += 1
        return tally != len(q)

    while checkQueue(queue):
        curNode = queue.pop(0)
        if curNode is None:
            queue.append(None)
            queue.append(None)
            tree.append("#")
        elif type(curNode) in [X, Y]:
            queue.append(None)
            queue.append(None)
            tree.append(str(curNode))
        else:
            queue.append(curNode.left)
            queue.append(curNode.right)
            tree.append(str(curNode.func))

    return tree, ceil(log(len(tree), 2))


def _printTree(tree, depth):
    s = ""
    for i in range(depth):
        numCom1 = 2 ** ((depth - 1) - i) - 1
        numCom2 = 2 ** (depth - i)
        numCom3 = numCom1 + 1
        s += ',' * numCom1
        for x in range(2 ** i):
            if len(tree) > 0:
                nodeVal = tree.pop(0)
                if nodeVal != '#':
                    s += nodeVal
            s += ',' * numCom2
        s += ',' * numCom3
        s += '\n'
    return s


def saveTree(root, filename):
    tree, depth = _createTree(root)
    with open("tests/{}".format(filename), 'w') as f:
        print(_printTree(tree, depth), end='', file=f)


if __name__ == '__main__':
    root = FunctionNode(.8)
    saveTree(root, 'test.csv')
    # Functions to add:
    #   Pascal's Triangle with mods
    #   Newton's method fractal (0)

