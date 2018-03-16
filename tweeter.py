import credentials
from random import randint
import markovify
import haiku

# Twitter credentials
api = credentials.api


def generateTweet():
    options = {
        'Batman': 'batman.json',
        'Bible': 'bible.json',
        'Common Sense': 'commonsense.json',
        'Dracula': 'dracula.json',
        'Brothers Grimm': 'grimms.json',
        'Kamasutra': 'kamasutra.json',
        'Moby Dick': 'mobydick.json',
        'Scarlet Letter': 'scarletletter.json'
    }
    keys = list(options.keys())
    i = randint(0, len(keys) - 1)
    with open('sources/{}'.format(options[keys[i]])) as f:
        model = markovify.Text.from_json(f.read())
    status = haiku.makeHaiku(model, keys[i])
    api.update_status(status=status)
    return status


def generateReply(handle):
    options = {
        'Batman': 'batman.json',
        'Bible': 'bible.json',
        'Common Sense': 'commonsense.json',
        'Dracula': 'dracula.json',
        'Brothers Grimm': 'grimms.json',
        'Kamasutra': 'kamasutra.json',
        'Moby Dick': 'mobydick.json',
        'Scarlet Letter': 'scarletletter.json'
    }
    keys = list(options.keys())
    i = randint(0, len(keys) - 1)
    with open('sources/{}'.format(options[keys[i]])) as f:
        model = markovify.Text.from_json(f.read())
    status = handle + '\n' + haiku.makeHaiku(model, keys[i])
    api.update_status(status=status)
    return status


if __name__ == '__main__':
    generateTweet()
