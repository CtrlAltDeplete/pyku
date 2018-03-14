import credentials
from random import randint
import markovify
import haiku

# Twitter credentials
api = credentials.api

if __name__ == '__main__':
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
    api.update_status(status=haiku.makeHaiku(model, keys[i]))
