import credentials
from random import randint
import markovify
import haiku

# Twitter credentials
api = credentials.api

# A dictionary for all the sources.
options = {
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
    'Dota 2': 'dota2.json'
}
keys = list(options.keys())
keys.sort()
# Add in random for source options.
keys.insert(0, 'Random')


# Handle is the user to tweet at, and source is the key for the file to base the model.
def generateTweet(handle='', source=["Random"]):
    models = []
    weights = []
    if len(source) > 3:
        source = source[:3]
    for s in source:
        # If random, choose a key randomly.
        if source == "Random":
            i = 1 + randint(0, len(keys) - 2)
            source = keys[i]
        # Create a model from the source.
        with open('sources/{}'.format(options[s])) as f:
            model = markovify.Text.from_json(f.read())
            with open('procTexts/{}'.format(options[s][:-4] + "txt"), 'r') as of:
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
    # Send the tweet,
    api.update_status(status=status)
    # And return the generated tweet.
    return status


if __name__ == '__main__':
    generateTweet()
