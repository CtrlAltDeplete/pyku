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
        return max(syllables, 1)
    return 0


def inText(text):
    syllables = 0
    for word in text.split():
        syllables += inWord(word)
    return syllables


if __name__ == '__main__':
    # singleSyl = "life, love, ER, world, ME, one, Day, AL, you, IN, tip, heart, on, Ate, no, Be, to, ay, AR, near, MA, en, CA, OR, la, Ta, Na, ch, ab, ad, ion, sh, MO, NE, DE, AN, ness, BA, Es, ring, ace, wolf, ap, go, fish, re, five, ae, man, and el"
    # for word in singleSyl.split():
    #     if inWord(word) != 1:
    #         print(word, inWord(word))
    # doubleSyl = "purple, perfect, silver, seven, thirteen, Godard, about, Thursday, again, Tuesday, pizza, thirty, donate, princess, people, water, future, Heaven, happy, sixty, country, pumpkin, Christmas, special, over, Angel, freedom, able, music, fifty, ana, thousand, fourteen, party, Monday, picture, office, language, nature, Kelly, city, Mumbai, woman, twenty, sugar, husband, anna,"
    # for word in doubleSyl.split():
    #     if inWord(word) != 2:
    #         print(word, inWord(word))
    # tripleSyl = "fireboard, family, chocolate, banana, assonant, Africa, happiness, piano, eleven, animal, Wednesday, seventy, Melissa, chipotle, celebrate, jessica, potato, business, favorite, elephant, erica, adventure, energy, history, Georgia, important, amazing, consonant, rihanna, India, feminine, ninety, dangerous, masculine, forever, Indian, holiday, syllable, abdicate, Madison, Canada, Jupiter, envelope, diamond, memory, together, media, Adrian,"
    # for word in tripleSyl.split():
    #     if inWord(word) != 3:
    #         print(word, inWord(word))
    # quadSyl = "identical, America, American, everything, January, undemanding, Virginia, Australia, irregular, aboveboard, information, Elizabeth, macaronic, intermittent, preposition, February, literature, secretary, Victoria, Amerindic, homecoming, independence, alligator, ordinary, syllabicate, alternative, technology, celebration, Carolina, maleficent, watermelon, Ariana, appreciate, community, relaxation, salmonella, forgiveness, aberration, vegetable, eternity, amelia, belligerent, angelica, retirement, television, intelligence"
    # for word in quadSyl.split():
    #     if inWord(word) != 4:
    #         print(word, inWord(word))
    for word in "And the whole heart.".split():
        print("{}, {}".format(word, inWord(word)))