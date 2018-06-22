import markovify
import re
import os


# Opens a raw text file and prepares it for everything else.
def processFile(filename):
    # Read the text in the file.
    try:
        with open("rawTexts/" + filename) as f:
            text = f.read()
    except UnicodeDecodeError:
        with open("rawTexts/" + filename, encoding="UTF8") as f:
            text = f.read()
    regex = re.compile('[^a-zA-Z\s,.!?]')
    text = regex.sub('', text)
    # Split on blank lines.
    data = text.split('\n')
    remove = []
    # Delete lines that are in all caps, likely directorial notes
    for i in range(len(data)):
        if data[i].upper() == data[i]:
            remove.insert(0, i)
    for i in remove:
        data.pop(i)
    # Split on blank space
    data = ' '.join(data).split()
    for i in range(len(data)):
        if data[i] in ['.', ',', '!', '?']:
            data[i] = ''
    data = ' '.join(data).split()
    # Write out the processed text to the same file.
    with open("procTexts/" + filename, 'w') as f:
        print(" ".join(data), file=f)


# Create and write a jsonModel for markovify.
def createCorpus(filename):
    # Read in the text file.
    corpus = open("procTexts/" + filename).read()
    # Create a model and turn it to json.
    textModel = markovify.Text(corpus, state_size=3, retain_original=False)
    modelJson = textModel.to_json()
    # Write out the json Model.
    with open("sources/" + filename[:-4] + ".json", 'w') as f:
        print(modelJson, file=f)


if __name__ == '__main__':
    # Process every file in the rawTexts directory.
    for filename in os.listdir("rawTexts"):
        processFile(filename)
    # Write a model for every file in the procTexts directory.
    for filename in os.listdir("procTexts"):
        createCorpus(filename)
