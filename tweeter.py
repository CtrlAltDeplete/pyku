import credentials
from random import randint
import markovify
import haiku

# Twitter credentials
api = credentials.api

options = {
    'Batman': 'batman.json',
    'Bible': 'bible.json',
    'Common Sense': 'commonsense.json',
    'Dracula': 'dracula.json',
    'Brothers Grimm': 'grimms.json',
    'Kamasutra': 'kamasutra.json',
    'Moby Dick': 'mobydick.json',
    'Scarlet Letter': 'scarletletter.json',
    'The Room': 'theroom.json'
}
keys = list(options.keys())


def generateTweet(handle=None, source=None):
    if not source:
        i = randint(0, len(keys) - 1)
        source = keys[i]
    with open('sources/{}'.format(options[source])) as f:
        model = markovify.Text.from_json(f.read())
    status = haiku.makeHaiku(model)
    status = "{}\n{}".format(status, source)
    if not handle:
        status = "{}\n{}".format(handle, status)
    api.update_status(status=status)
    return status


if __name__ == '__main__':
    generateTweet()
