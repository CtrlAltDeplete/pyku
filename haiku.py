import syllables
import markovify
from random import randint
import os


def splitAt(line, goal):
    line = line.split()
    cur = []
    count = 0
    for word in line:
        count += syllables.syllablesInWord(word)
        cur.append(word)
        if count == goal:
            line, excess = ' '.join(cur), ' '.join(line[len(cur):])
            if excess == '':
                excess = None
            return line, excess
        elif count > goal:
            return None, None


def makeHaiku(model):
    while True:
        max_chars = randint(80, 120)
        line = None
        while not line:
            line = model.make_short_sentence(max_chars=max_chars, tries=100)
        while syllables.syllablesInString(line) < 17:
            max_chars -= randint(20, 40)
            newSent = None
            while not newSent:
                newSent = model.make_short_sentence(max_chars=max_chars, tries=100)
            line += ' ' + newSent
        if syllables.syllablesInString(line) == 17:
            line1, excess = splitAt(line, 5)
            if line1:
                line2, excess = splitAt(excess, 7)
                if line2:
                    return "{}\n{}\n{}".format(line1, line2, excess)


if __name__ == '__main__':
    # for filename in os.listdir("sources"):
    #     with open("sources/{}".format(filename)) as f:
    #         model = markovify.Text.from_json(f.read())
    #     print(makeHaiku(model))
    #     print('-' * 30)
    with open("sources/batman.json") as f:
        model = markovify.Text.from_json(f.read())
    print(makeHaiku(model))
