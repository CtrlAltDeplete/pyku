import os
import re


# Opens a raw text file and prepares it for everything else.
def processFile(filename):
    # Read the text in the file.
    try:
        with open("rawTexts/" + filename) as f:
            text = f.read()
    except UnicodeDecodeError:
        with open("rawTexts/" + filename, encoding="UTF8") as f:
            text = f.read()
    regex = re.compile('[^a-zA-Z ]')
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
    data = ' '.join(data).lower().split()
    # Write out the processed text to the same file.
    with open("rawTexts/" + filename, 'w') as f:
        print(" ".join(data), file=f)


if __name__ == '__main__':
    # Process every file in the rawTexts directory.
    for filename in os.listdir("rawTexts"):
        processFile(filename)
