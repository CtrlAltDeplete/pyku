import credentials
import markovify
import haiku
from artCreator import *
from os import remove
from random import seed


# Twitter credentials
api = credentials.api

# A dictionary for all the sources.
options = {
    'American Psycho': 'americanpsycho.json',
    'Batman': 'batman.json',
    'Bible': 'bible.json',
    'The Great Gatsby': 'greatgatsby.json',
    'Moby Dick': 'mobydick.json',
    'The Room (Original Script)': 'theroom.json',
    'Infinite Jest': 'infinitejest.json',
    'Blue Velvet': 'bluevelvet.json',
    'War And Peace': 'warandpeace.json',
    'Nineteen Eighty Four': '1984.json',
    'Brave New World': 'bravenewworld.json',
    'Farewell To Arms': 'farewelltoarms.json',
    'Dota 2 Lore': 'dota2lore.json',
    'Dota 2 Reviews': 'dota2reviews.json',
    'Iliad': 'iliad.json',
    'Shrek': 'shrek.json',
    'Paradise Lost': 'paradiselost.json',
    'Fear And Loathing In Las Vegas': 'fearandloathing.json',
    'Trump Tweets': 'trumptweets.json'
}
keys = list(options.keys())
keys.sort()
# Add in random for source options.
keys.insert(0, 'Random')


# Handle is the user to tweet at, and source is the key for the file to base the model.
def generateTweetWithImage(handle='', source=["Random"], send=True, delete=True):
    models = []
    weights = []
    if len(source) > 3:
        source = source[:3]
    for i in range(len(source)):
        # If random, choose a key randomly.
        if source[i] == "Random":
            j = 1 + randint(0, len(keys) - 2)
            source[i] = keys[j]
        # Create a model from the source.
        with open('sources/{}'.format(options[source[i]])) as f:
            model = markovify.Text.from_json(f.read())
            try:
                with open('rawTexts/{}'.format(options[source[i]][:-4] + "txt"), 'r') as of:
                    weights.append(len(of.read()))
            except UnicodeDecodeError:
                with open('rawTexts/{}'.format(options[source[i]][:-4] + "txt"), 'r', encoding='utf8') as of:
                    weights.append(len(of.read()))
        models.append(model)
    if len(models) > 1:
        total = 0
        for w in weights:
            total += w
        for i in range(len(weights)):
            weights[i] = int(total / weights[i])
        model = markovify.combine(models, weights)
    else:
        model = models[0]
    # Generate a haiku (and format it).
    poem = haiku.makeHaiku(model)
    status = poem
    status = "{}\n#{}".format(status, ' #'.join(''.join(s.split()) for s in source))
    # Insert the handle at the beginning if needed.
    if handle != '':
        status = "{}\n{}".format(handle, status)
    seed(poem)
    # Generate the art to attach to the tweet.
    imgName = createAttachment("test", poem)
    # Send the tweet, if desired
    if send:
        tweet = api.update_with_media(imgName, status=status)
    if delete:
        remove(imgName)
    # And return the generated tweet.
    if send:
        return status, tweet.entities['media'][0]['media_url']
    return status, imgName


# Handle is the user to tweet at, and source is the key for the file to base the model.
def generateTweet(handle='', source=["Random"], send=True):
    models = []
    weights = []
    if len(source) > 3:
        source = source[:3]
    for i in range(len(source)):
        # If random, choose a key randomly.
        if source[i] == "Random":
            j = 1 + randint(0, len(keys) - 2)
            source[i] = keys[j]
        # Create a model from the source.
        with open('sources/{}'.format(options[source[i]])) as f:
            model = markovify.Text.from_json(f.read())
            try:
                with open('rawTexts/{}'.format(options[source[i]][:-4] + "txt"), 'r') as of:
                    weights.append(len(of.read()))
            except UnicodeDecodeError:
                with open('rawTexts/{}'.format(options[source[i]][:-4] + "txt"), 'r', encoding='utf8') as of:
                    weights.append(len(of.read()))
        models.append(model)
    if len(models) > 1:
        total = 0
        for w in weights:
            total += w
        for i in range(len(weights)):
            weights[i] = int(total / weights[i])
        model = markovify.combine(models, weights)
    else:
        model = models[0]
    # Generate a haiku (and format it).
    status = haiku.makeHaiku(model)
    status = "{}\n#{}".format(status, ' #'.join(''.join(s.split()) for s in source))
    # Insert the handle at the beginning if needed.
    if handle != '':
        status = "{}\n{}".format(handle, status)
    # Send the tweet, if desired
    if send:
        api.update_status(status)
    # And return the generated tweet.
    return status


if __name__ == '__main__':
    generateTweetWithImage()
