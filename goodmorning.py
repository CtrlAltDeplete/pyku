from artCreator import *
from os import remove
import credentials


def sayGoodmorning():
    palette = choice(palettes)
    cHead = FunctionNode(randint(70, 100) / 100)
    finalImage = PaletteImage(1024, 512, cHead, palette)
    font = choice(list(font_params.keys()))
    fontSize = randint(font_params[font] * 2, int(font_params[font] * 2.5))
    effectedPixels, dx, dy = createText(1024, 512, "Good Morning", font, fontSize)
    drawText(effectedPixels, dx, dy, finalImage.canvas)
    finalImage.save("goodmorning.png")

    api = credentials.api
    api.update_with_media("goodmorning.png")
    remove("goodmorning.png")


if __name__ == '__main__':
    sayGoodmorning()
