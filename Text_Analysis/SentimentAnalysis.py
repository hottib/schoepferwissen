from textblob_de import TextBlobDE as TextBlob

def getSentiment(filename):
    with open(filename, "r") as f:
        text = str(f.readlines())
    blob = TextBlob(text)
    return blob.sentiment