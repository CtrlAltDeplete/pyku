from artCreator import *
from os import remove
import credentials
from datetime import datetime


def sayGoodnight():
    createAttachment("goodnight", "Goodnight", s=datetime())

    api = credentials.api
    api.update_with_media("goodnight.png")
    remove("goodnight.png")


if __name__ == '__main__':
    sayGoodnight()
