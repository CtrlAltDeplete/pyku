import syllables
import markovify
import os


def split12(line):
    words = line.split()
    line1, line2 = '', ''
    for i in range(1, len(words) + 1):
        if syllables.syllablesInString(' '.join(words[:i])) == 5:
            line1 = ' '.join(words[:i])
            line2 = ' '.join(words[i:])
            return True, line1, line2
    return False, line1, line2


def split123(line):
    words = line.split()
    line1, line2, line3 = '', '', ''
    for i in range(1, len(words) + 1):
        if syllables.syllablesInString(' '.join(words[:i])) == 5:
            line1 = ' '.join(words[:i])
            words = words[i:]
            break
    if line1 != '':
        for i in range(1, len(words) + 1):
            if syllables.syllablesInString(' '.join(words[:i])) == 7:
                line2 = ' '.join(words[:i])
                line3 = ' '.join(words[i:])
                return True, line1, line2, line3
    return False, line1, line2, line3


def split23(line):
    words = line.split()
    line2, line3 = '', ''
    for i in range(1, len(words) + 1):
        if syllables.syllablesInString(' '.join(words[:i])) == 7:
            line2 = ' '.join(words[:i])
            line3 = ' '.join(words[i:])
            return True, line2, line3
    return False, line2, line3


def makeHaiku(model):
    line = model.make_short_sentence(max_chars=150, tries=100)
    while True:
        count = syllables.syllablesInString(line)
        if count == 5:
            return line + '\n' + secondLine(model)
        elif count == 12:
            splittable, line1, line2 = split12(line)
            if splittable:
                return line1 + '\n' + line2 + '\n' + thirdLine(model)
        elif count == 17:
            splittable, line1, line2, line3 = split123(line)
            if splittable:
                return line1 + '\n' + line2 + '\n' + line3
        line = model.make_short_sentence(max_chars=150, tries=100)


def secondLine(model):
    line = model.make_short_sentence(max_chars=100, tries=100)
    while True:
        count = syllables.syllablesInString(line)
        if count == 7:
            return line + '\n' + thirdLine(model)
        elif count == 12:
            splittable, line2, line3 = split23(line)
            if splittable:
                return line2 + '\n' + line3
        line = model.make_short_sentence(max_chars=100, tries=100)


def thirdLine(model):
    line = model.make_short_sentence(max_chars=50, tries=100)
    count = syllables.syllablesInString(line)
    while count != 5:
        line = model.make_short_sentence(max_chars=50, tries=100)
        count = syllables.syllablesInString(line)
    return line


if __name__ == '__main__':
    # for filename in os.listdir("sources"):
    #     with open("sources/{}".format(filename)) as f:
    #         model = markovify.Text.from_json(f.read())
    #     print(makeHaiku(model))
    #     print('-' * 30)
    with open("sources/scottwalker.json") as f:
        model = markovify.Text.from_json(f.read())
    print(makeHaiku(model))
