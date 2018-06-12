import markovify
import os


# Create and write a jsonModel for markovify.
def createCorpus(filename):
    # Read in the text file.
    corpus = open("procTexts/" + filename).read()
    # Create a model and turn it to json.
    textModel = markovify.Text(corpus, state_size=3)
    modelJson = textModel.to_json()
    # Write out the json Model.
    with open("sources/" + filename[:-4] + ".json", 'w') as f:
        print(modelJson, file=f)


if __name__ == '__main__':
    # Write a model for every file in the procTexts directory.
    # for filename in os.listdir("procTexts"):
    #     createCorpus(filename)
    createCorpus("dota2lore.txt")
