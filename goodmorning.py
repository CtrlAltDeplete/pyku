from artCreator import *
from os import remove
import credentials
from datetime import datetime


def sayGoodmorning():
    createAttachment("goodmorning", "Good Morning", s=datetime())

    api = credentials.api
    api.update_with_media("goodmorning.png")
    remove("goodmorning.png")


if __name__ == '__main__':
    sayGoodmorning()
