import re


def inWord(word):
    regex = re.compile('[^a-zA-Z]')
    word = regex.sub('', word)
    word = word.lower()
    syllables = 0
    if len(word) > 0:
        for i in range(len(word)):
            if i != 0:
                if word[i] in 'aeiouy' and word[i - 1] not in 'aeiouy':
                    syllables += 1
                elif i + 1 < len(word) and word[i - 1] in 'aeiou' and word[i] == 'y' and word[i + 1] in 'aeiou':
                    syllables += 1
            elif word[i] in 'aeiouy':
                syllables += 1
        if word[-1] == 'e':
            if len(word) >= 3 and ((word[-2] != 'l' and syllables > 1 and word[-3] in 'aeiouyd') or word[-3:-1] == 'nn'):
                syllables -= 1
        if len(word) > 3 and word[-3] not in 'aeiouys' and word[-2:] == 'es' and word[-4:] not in ['ches', 'shes'] and word[-3:] != 'ces':
            syllables -= 1
        if len(word) > 3 and word[-4] in 'aeiouy' and word[-3:] == 'sed':
            syllables -= 1
        if len(word) > 4 and word[2] in 'aeiouy' and word[:2] in ['re', 'tri', 'bi']:
            syllables += 1
        if len(word) > 4 and word[-4:] == 'ened':
            syllables -= 1
        syllables += word.count('ia')
        syllables -= word.count('tia')
        syllables -= (word.count('cia') - word.count('ciate'))
        syllables += word.count('ying')
        syllables += word.count('aing')
        syllables += word.count('eing')
        syllables += word.count('oing')
        syllables += word.count('uing')
        syllables += word.count('uar')
        syllables += word.count('dnt')
        syllables += word.count('snt')
        syllables += word.count('dn\'t')
        syllables += word.count('sn\'t')
        syllables -= word.count('used')
        syllables -= word.count('ushed')
        syllables -= word.count('eigned')
        syllables += word.count('uate')
        syllables -= word.count('ened')
        syllables += word.count('idea')
        syllables += word.count('ybe')
        syllables += word.count('ious')
        syllables -= word.count('erned')
        syllables -= word.count('ouched')
        syllables -= word.count('oyed')
        syllables -= word.count('hole')
        syllables -= word.count('where')
        syllables += word.count('were')
        syllables -= word.count('hale')
        syllables -= word.count('iage')
        syllables -= word.count('eyes')
        syllables -= word.count('pped')
        return max(syllables, 1)
    return 0


def inText(text):
    syllables = 0
    for word in text.split():
        syllables += inWord(word)
    return syllables


if __name__ == '__main__':
    for word in "but thou art shipped".split():
        print("{}, {}".format(word, inWord(word)))