import credentials
import markovify
import tweepy
import haiku
import json

# Twitter credentials
api = tweepy.API(credentials.auth)


# Function for building and returning a model
def buildModel(source):
    with open('source/{}Json.txt'.format(source)) as f:
        model = markovify.Text.from_json(f.read())
    return model

keywords = {
    'batman': 'batman',
    'bat': 'batman',
    'dark': 'batman',
    'knight': 'batman',
    'beowulf': 'beowulf',
    'wulf': 'beowulf',
    'bible': 'bible',
    'jesus': 'bible',
    'christ': 'bible',
    'god': 'bible',
    'commonsense': 'commonsense',
    'common': 'commonsense',
    'sense': 'commonsense',
    'thomas': 'commonsense',
    'pain': 'commonsense',
    'dracula': 'dracula',
    'brothersgrimm': 'grimms',
    'brother': 'grimms',
    'grimm': 'grimms',
    'kamasutra': 'kamasutra',
    'kama': 'kamasutra',
    'sutra': 'kamasutra',
    'mobydick': 'mobydick',
    'moby': 'mobydick',
    'dick': 'mobydick',
    'whale': 'mobydick',
    'scarletletter': 'scarletletter',
    'scarlet': 'scarletletter',
    'letter': 'scarletletter'
}

def generateTweet(source):
    with open('sources/{}.json'.format(source)) as f:
        model = markovify.Text.from_json(f.read())
    return haiku.makeHaiku(model)


class StdOutListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        tweet = json.loads(raw_data)
        screen_name = tweet['user']['screen_name']
        text = tweet['text'][14:].lower()
        id = tweet['id']

        source = None
        for key in keywords.keys():
            if key in text:
                source = keywords[key]
                break

        if source:
            t = "@{}\n{}".format(screen_name, generateTweet(source))
            api.update_status(status=t, in_reply_to_status_id=id)

        return True

    def on_error(self, status):
        api.update_status(status=status)


if __name__ == '__main__':
    l = StdOutListener()
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['@TrashPostBot'])
