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
    '1984': '1984.json',
    'Brave New World': 'bravenewworld.json',
    'Farewell To Arms': 'farewelltoarms.json'
}
keys = list(options.keys())
keys.sort()
# Add in random for source options.
keys.insert(0, 'Random')


# Handle is the user to tweet at, and source is the key for the file to base the model.
def generateTweet(handle='', source="Random"):
    # If random, choose a key randomly.
    if source == "Random":
        i = 1 + randint(0, len(keys) - 2)
        source = keys[i]
    # Create a model from the source.
    with open('sources/{}'.format(options[source])) as f:
        model = markovify.Text.from_json(f.read())
    # Generate a haiku (and format it).
    status = haiku.makeHaiku(model)
    status = "{}\n#{}".format(status, ''.join(source.split()))
    # Insert the handle at the beginning if needed.
    if handle != '':
        status = "{}\n{}".format(handle, status)
    # Send the twee,
    api.update_status(status=status)
    # And return the generated tweet.
    return status


if __name__ == '__main__':
    generateTweet()
