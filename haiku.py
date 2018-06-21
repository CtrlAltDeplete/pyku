import syllables
import markovify
import os


# Splits a 12 syllable line into a 5 and 7 if possible.
def split12(line):
    words = line.split()
    line1, line2 = '', ''
    # Iterate through the words in line,
    for i in range(1, len(words) + 1):
        # If the syllable count is exactly 5, split the line at this word.
        if syllables.syllablesInString(' '.join(words[:i])) == 5:
            line1 = ' '.join(words[:i])
            line2 = ' '.join(words[i:])
            # Return true for a valid split and the resulting lines.
            return True, line1, line2
    # Return false if a valid split was not possible.
    return False, line1, line2


# Splits a 17 syllable line into a 5, 7, and 5 if possible.
def split123(line):
    words = line.split()
    line1, line2, line3 = '', '', ''
    # Iterate through the words in line,
    for i in range(1, len(words) + 1):
        # If the syllable count is exactly 5, split the first line at this word.
        if syllables.syllablesInString(' '.join(words[:i])) == 5:
            line1 = ' '.join(words[:i])
            words = words[i:]
            break
    # Check to make sure a first line was successfully made,
    if line1 != '':
        # Iterate through the remaining words in line,
        for i in range(1, len(words) + 1):
            # If the syllable count is exactly 7, split the second and third lines at this word.
            if syllables.syllablesInString(' '.join(words[:i])) == 7:
                line2 = ' '.join(words[:i])
                line3 = ' '.join(words[i:])
                # Return true for a valid split and the resulting lines.
                return True, line1, line2, line3
    # Return false if a valid split was not possible.
    return False, line1, line2, line3


# Splits a 12 syllable line into a 7 and 5 if applicable.
def split23(line):
    words = line.split()
    line2, line3 = '', ''
    # Iterate through the words in line,
    for i in range(1, len(words) + 1):
        # If the syllable count is exactly 7, split the line at this word.
        if syllables.syllablesInString(' '.join(words[:i])) == 7:
            line2 = ' '.join(words[:i])
            line3 = ' '.join(words[i:])
            # Return true for a valid split and the resulting lines.
            return True, line2, line3
    # Return false if a valid split was not possible.
    return False, line2, line3


def makeHaiku(model):
    # Generate a line with the markov model passed.
    line = model.make_short_sentence(max_chars=150, tries=100)
    while True:
        # Count the number of syllables in the generated line.
        count = syllables.syllablesInString(line)
        # If the count is 5, we have the first line of the haiku.
        if count == 5:
            # Return our first line with a generated second line.
            return line + '\n' + secondLine(model)
        # If the count is 12, we might have our first and second line.
        elif count == 12:
            # Check if the line is splittable,
            splittable, line1, line2 = split12(line)
            if splittable:
                # And if it is, return the split lines with a third line.
                return line1 + '\n' + line2 + '\n' + thirdLine(model)
        # If the count is 17, we might have our full haiku.
        elif count == 17:
            # Check if the line is splittable,
            splittable, line1, line2, line3 = split123(line)
            if splittable:
                # And if it is, return the split lines as the haiku.
                return line1 + '\n' + line2 + '\n' + line3
        # If the syllable count was no good, or if the line wasn't splittable, generate a new line.
        line = model.make_short_sentence(max_chars=150, tries=100)


def secondLine(model):
    # Generate a line with the markov model passed.
    line = model.make_short_sentence(max_chars=100, tries=100)
    while True:
        # Count the number of syllables in the generated line.
        count = syllables.syllablesInString(line)
        # If the count is 7, we have the second line of the haiku.
        if count == 7:
            # Return our second line with a generated third line.
            return line + '\n' + thirdLine(model)
        # If the count is 12, we might have our second and third line.
        elif count == 12:
            # Check if the line is splittable,
            splittable, line2, line3 = split23(line)
            if splittable:
                # And if it is, return the split lines.
                return line2 + '\n' + line3
        # If the syllable count was no good, or if the line wasn't splittable, generate a new line.
        line = model.make_short_sentence(max_chars=100, tries=100)


def thirdLine(model):
    # Generate a line with the markov model passed.
    line = model.make_short_sentence(max_chars=50, tries=100)
    # Count the number of syllables in the generated line.
    count = syllables.syllablesInString(line)
    # Repeat this process until the line has exactly 5 syllables,
    while count != 5:
        line = model.make_short_sentence(max_chars=50, tries=100)
        count = syllables.syllablesInString(line)
    # Then return this line.
    return line


if __name__ == '__main__':
    # for filename in os.listdir("sources"):
    #     with open("sources/{}".format(filename)) as f:
    #         model = markovify.Text.from_json(f.read())
    #     print(makeHaiku(model))
    #     print('-' * 30)
    with open("sources/dota2lore.json") as f:
        model = markovify.Text.from_json(f.read())
    print(makeHaiku(model))
