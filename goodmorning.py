from artCreator import *
from os import remove
import credentials
from datetime import date


def sayGoodmorning():
    createAttachment("Good Morning", "goodmorning", date.today())

    api = credentials.api
    api.update_with_media("goodmorning.png")
    remove("goodmorning.png")


if __name__ == '__main__':
    sayGoodmorning()
