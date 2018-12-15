import credentials

from ArtCreator import *
from datetime import date
from os import remove


def say_goodnight():
    create_attachment("Goodnight", "goodnight", date.today())

    api = credentials.api
    api.update_with_media("goodnight.png")
    remove("goodnight.png")


if __name__ == '__main__':
    say_goodnight()
