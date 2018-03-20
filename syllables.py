import re

consonants = {}
vowels = {}
rvowels = {}
exceptions = {}

# Populate the phoneme dictionaries with data
with open("phonemeData.txt", 'r') as f:
    data = f.read()
    data = data.split()
    for i in range(18):
        graphemes = data[i].split(':')[0].split(',')
        phoneme = data[i].split(':')[1]
        for gr in graphemes:
            if gr not in consonants:
                if "_" in gr:
                    for ch in "bcdfghjklmnpqrstvwxz":
                        if gr.replace("_", ch) not in consonants:
                            consonants[gr.replace("_", ch)] = phoneme
                else:
                    consonants[gr] = phoneme
    for i in range(18, 33):
        graphemes = data[i].split(':')[0].split(',')
        phoneme = data[i].split(':')[1]
        for gr in graphemes:
            if gr not in vowels:
                if "_" in gr:
                    for ch in "bcdfghjklmnpqrstvwxz":
                        if gr.replace("_", ch) not in vowels:
                            vowels[gr.replace("_", ch)] = phoneme
                else:
                    vowels[gr] = phoneme
    for i in range(33, 39):
        graphemes = data[i].split(':')[0].split(',')
        phoneme = data[i].split(':')[1]
        for gr in graphemes:
            if gr not in rvowels:
                if "_" in gr:
                    for ch in "bcdfghjklmnpqrstvwxz":
                        if gr.replace("_", ch) not in rvowels:
                            rvowels[gr.replace("_", ch)] = phoneme
                else:
                    rvowels[gr] = phoneme
    for i in range(39, len(data)):
        exception = data[i].split(':')[0]
        mult = int(data[i].split(':')[1])
        exceptions[exception] = mult


def findPhoneme(graph):
    if graph in vowels:
        return vowels[graph], 1
    if graph in rvowels:
        return rvowels[graph], 1
    if graph in consonants:
        return consonants[graph], 0
    return None


def breakdownWord(word):
    regex = re.compile('[^a-zA-Z]')
    word = regex.sub('', word)
    word = word.lower()
    phonemes = []
    for i in reversed(range(1, min(len(word) + 1, 5))):
        part = word[:i]
        pho = findPhoneme(part)
        if pho and part == word:
            phonemes.append(pho)
            return phonemes
        elif pho:
            phonemes.append(pho)
            phonemes.extend(breakdownWord(word[i:len(word)]))
            return phonemes


def syllablesInWord(word):
    phonemes = breakdownWord(word)
    count = 0
    for i in range(len(phonemes)):
        count += phonemes[i][1]
        if i != 0:
            if phonemes[i][0] == '/e/' and phonemes[i - 1][0] == '/schwa/':
                count -= 1
    for key in exceptions:
        count += word.count(key) * exceptions[key]
    return max(1, count)


def syllablesInString(text):
    syllables = 0
    for word in text.split():
        syllables += syllablesInWord(word)
    return syllables


if __name__ == '__main__':
    for word in "test string".split():
        print("{}, {}".format(word, syllablesInWord(word)))
