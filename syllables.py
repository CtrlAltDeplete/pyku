import re


with open("rules.txt") as f:
    rules = f.read().split()
    diphthongs = rules[0].split(',')
    digraphs = rules[1].split(',')
    onePrefixes = rules[2].split(',')
    twoPrefixes = rules[3].split(',')
    oneSuffixes = rules[4].split(',')
    twoSuffixes = rules[5].split(',')
consonants = "bcdfghjklmnpqrstvwxyz"
vowels = "aeiouy"


def countVowels(part):
    count = 0
    for ch in part:
        if ch in vowels:
            count += 1
    return count


def syllablesInPart(part):
    count = countVowels(part)
    if part[-1] == 'e':
        part = part[:-1]
        count -= 1
    for dip in diphthongs:
        if dip in part:
            count -= countVowels(dip) - 1
    return max(0, count)


def syllablesInWord(word):
    regex = re.compile('[^a-zA-Z]')
    word = regex.sub('', word)
    word = word.lower()
    if len(word) == 0:
        return 0
    parts = []
    count = 0
    split = True
    if word[-1] == 's':
        word = word[:-1]
        if len(word) >= 4 and word[-4:] in ['tche', 'esse', 'asse']:
            count += 1
    if len(word) > 3 and word[-2:] == 'le' and word[-3] in consonants:
        count += 1
        word = word[:-3]
    if len(word) > 5 and word[-2:] == 'ed' and word[-3] != 'd' and word[-3] in consonants:
        word = word[:-3]
    if len(word) > 5 and word[-5:] in ['tched'] or word[-4:] in ['shed', 'osed']:
        count -= 1
    while split:
        split = False
        for twoPre in twoPrefixes:
            if len(twoPre) < len(word):
                if word[:len(twoPre)] == twoPre:
                    word = word[len(twoPre):]
                    count += 2
                    split = True
        for onePre in onePrefixes:
            if len(onePre) < len(word):
                if word[:len(onePre)] == onePre:
                    word = word[len(onePre):]
                    count += 1
                    split = True
        for twoSuf in twoSuffixes:
            if len(twoSuf) < len(word):
                if word[-len(twoSuf):] == twoSuf:
                    word = word[:-len(twoSuf)]
                    count += 2
                    split = True
        for suf in oneSuffixes:
            if len(suf) < len(word):
                if word[-len(suf):] == suf:
                    word = word[:-len(suf)]
                    count += 1
                    split = True
    odd = len(word) % 2 == 1
    mid = len(word) // 2
    if not odd and len(word) >= 4:
        if countVowels(word[mid - 1:mid + 1]) == 0 and word[mid - 1:mid + 1] not in digraphs and countVowels(word[mid - 2:mid + 2]) == 2:
            parts.append(word[:mid])
            parts.append(word[mid:])
            word = ''
        elif countVowels(word[mid - 1:mid + 2]) == 2 and word[mid] in consonants:
            parts.append(word[:mid])
            parts.append(word[mid:])
            word = ''
    elif odd and len(word) >= 5:
        if countVowels(word[mid - 1:mid + 1]) == 0 and word[mid - 1:mid + 1] not in digraphs and countVowels(word[mid - 2:mid + 2]) == 2:
            parts.append(word[:mid])
            parts.append(word[mid:])
            word = ''
        elif countVowels(word[mid:mid + 3]) == 2 and word[mid + 1] in consonants:
            parts.append(word[:mid + 1])
            parts.append(word[mid + 1:])
            word = ''
    if word != '':
        parts.append(word)
    for part in parts:
        count += syllablesInPart(part)
    return max(count, 1)


def syllablesInString(text):
    count = 0
    for word in text.split():
        count += syllablesInWord(word)
    return count


if __name__ == '__main__':
    for word in "slammed".split():
        print(word, syllablesInWord(word))
