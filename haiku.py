import syllables
import markovify
import os


def makeHaiku(model):
    line = model.make_short_sentence(max_chars=140, tries=100)
    while syllables.syllablesInString(line) != 5:
        line = model.make_short_sentence(max_chars=140, tries=100)
    haiku = line + '\n'
    while syllables.syllablesInString(line) != 7:
        line = model.make_short_sentence(max_chars=140, tries=100)
    haiku += line + '\n'
    while syllables.syllablesInString(line) != 5:
        line = model.make_short_sentence(max_chars=140, tries=100)
    haiku += line
    return haiku


if __name__ == '__main__':
    for filename in os.listdir("sources"):
        with open("sources/{}".format(filename)) as f:
            model = markovify.Text.from_json(f.read())
        print(makeHaiku(model))
