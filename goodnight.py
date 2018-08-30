from artCreator import *
from os import remove
import credentials


def sayGoodnight():
    palette = choice(palettes)
    cHead = FunctionNode(randint(70, 100) / 100)
    finalImage = PaletteImage(1024, 512, cHead, palette)
    font = choice(list(font_params.keys()))
    fontSize = randint(font_params[font]['min'], font_params[font]['max']) * 2
    effectedPixels, dx, dy = createText(1024, 512, "Goodnight", font, fontSize)
    drawText(effectedPixels, dx, dy, finalImage.canvas)
    finalImage.save("goodnight.png")

    api = credentials.api
    api.update_with_media("goodnight.png")
    remove("goodnight.png")


if __name__ == '__main__':
    sayGoodnight()
