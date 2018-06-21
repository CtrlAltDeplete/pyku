import syllables
import markovify
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
    result = None
    while not result:
        lines = []
        genLine = None
        while not genLine:
            genLine = model.make_short_sentence(max_chars=100, tries=500)
        line, excess = splitAt(genLine, 5)
        # Split of first line was successful.
        if line:
            # Add the result to lines.
            lines.append(line)
            # If there is excess, handle it.
            if excess:
                # If enough excess for next line, use it.
                if syllables.syllablesInString(excess) >= 7:
                    line, excess = splitAt(excess, 7)
                # Otherwise, concatenate more generation.
                else:
                    genLine = None
                    while not genLine:
                        genLine = model.make_short_sentence(max_chars=70, tries=500)
                    excess += ' ' + genLine
                    line, excess = splitAt(excess, 7)
            # Otherwise, generate a new line.
            else:
                while not excess:
                    excess = model.make_short_sentence(max_chars=85, tries=500)
                line, excess = splitAt(excess, 7)
            if line:
                # Add the result to lines.
                lines.append(line)
                # If there is excess, handle it.
                if excess:
                    # If enough excess for next line, use it.
                    if syllables.syllablesInString(excess) >= 5:
                        line, excess = splitAt(excess, 5)
                    # Otherwise, concatenate more generation.
                    else:
                        genLine = None
                        while not genLine:
                            genLine = model.make_short_sentence(max_chars=40, tries=500)
                        excess += ' ' + genLine
                        line, excess = splitAt(excess, 5)
                # Otherwise, generate a new line.
                else:
                    while not excess:
                        excess = model.make_short_sentence(max_chars=55, tries=500)
                    line, excess = splitAt(excess, 5)
                if line:
                    # Add the result to lines.
                    lines.append(line)
                    # If there is excess, the haiku does not work.
                    if not excess:
                        result = '\n'.join(lines)
    return result


if __name__ == '__main__':
    # for filename in os.listdir("sources"):
    #     with open("sources/{}".format(filename)) as f:
    #         model = markovify.Text.from_json(f.read())
    #     print(makeHaiku(model))
    #     print('-' * 30)
    with open("sources/modestproposal.json") as f:
        model = markovify.Text.from_json(f.read())
    print(makeHaiku(model))
