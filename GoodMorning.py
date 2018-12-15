import credentials

from ArtCreator import *
from datetime import date
from os import remove


def say_goodmorning():
    create_attachment("Good Morning", "goodmorning", date.today())

    api = credentials.api
    api.update_with_media("goodmorning.png")
    remove("goodmorning.png")


if __name__ == '__main__':
    say_goodmorning()
