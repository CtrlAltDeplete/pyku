import markovify
import os
import Syllables
import time


def split_at(line, goal):
    line = line.split()
    cur = []
    count = 0
    for word in line:
        count += Syllables.syllablesInWord(word)
        cur.append(word)
        if count == goal:
            line, excess = ' '.join(cur), ' '.join(line[len(cur):])
            if excess == '':
                excess = None
            return line, excess
        elif count > goal:
            return None, None


def make_haiku(model):
    while True:
        line = None
        while not line:
            line = model.make_short_sentence(max_chars=100, tries=100)
        while Syllables.syllablesInString(line) < 17:
            new_sent = None
            while not new_sent:
                new_sent = model.make_short_sentence(max_chars=30, tries=100)
            line += ' ' + new_sent
        if Syllables.syllablesInString(line) == 17:
            line1, excess = split_at(line, 5)
            if line1:
                line2, excess = split_at(excess, 7)
                if line2:
                    return "{}\n{}\n{}".format(line1, line2, excess)


if __name__ == '__main__':
    for filename in os.listdir("sources"):
        if filename not in ['commonsense.json', 'modestproposal.json', 'scottwalker.json']:
            with open("sources/{}".format(filename)) as f:
                model = markovify.Text.from_json(f.read())
            all_times = []
            for i in range(100):
                start = time.time()
                make_haiku(model)
                all_times.append(time.time() - start)
            print("Average: {}".format(sum(all_times) / 100))
            print("Maximum: {}".format(max(all_times)))
