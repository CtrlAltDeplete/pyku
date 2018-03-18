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
    'The Great Gatsby': 'greatgatsby.json',
    'Brothers Grimm': 'grimms.json',
    'Kamasutra': 'kamasutra.json',
    'Moby Dick': 'mobydick.json',
    'The Room': 'theroom.json',
    'Scarlet Letter': 'scarletletter.json'
}
keys = list(options.keys())
keys.insert(0, 'Random')


def generateTweet(handle='', source="Random"):
    if source == "Random":
        i = randint(0, len(keys) - 2)
        source = keys[i]
    with open('sources/{}'.format(options[source])) as f:
        model = markovify.Text.from_json(f.read())
    status = haiku.makeHaiku(model)
    status = "{}\n#{}".format(status, ''.join(source.split()))
    if handle != '':
        status = "{}\n{}".format(handle, status)
    api.update_status(status=status)
    return status


if __name__ == '__main__':
    generateTweet()
