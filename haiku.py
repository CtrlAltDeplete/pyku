import syllables
import markovify
import os


def makeHaiku(model):
    line = model.make_short_sentence(max_chars=140, tries=100)
    while syllables.inText(line) != 5:
        line = model.make_short_sentence(max_chars=140, tries=100)
    haiku = line + '\n'
    while syllables.inText(line) != 7:
        line = model.make_short_sentence(max_chars=140, tries=100)
    haiku += line + '\n'
    while syllables.inText(line) != 5:
        line = model.make_short_sentence(max_chars=140, tries=100)
    haiku += line
    return haiku


if __name__ == '__main__':
    for filename in os.listdir("sources"):
        with open("sources/" + filename) as f:
            print(makeHaiku(markovify.Text.from_json(f.read())))
