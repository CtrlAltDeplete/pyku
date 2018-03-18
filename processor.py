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
    # Split on blank lines.
    data = text.split()
    # Iterate through every word and remove bad symbols.
    for i in range(len(data)):
        for char in "@#$%^&*()_=+[{]}\\|;:\"<>/`~0123456789":
            data[i] = data[i].replace(char, "")
    # Write out the processed text to the same file.
    with open("rawTexts/" + filename, 'w') as f:
        print(" ".join(data), file=f)


if __name__ == '__main__':
    # Process every file in the rawTexts directory.
    # for filename in os.listdir("rawTexts"):
    #     processFile(filename)
    processFile("greatgatsby.txt")
