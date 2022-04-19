import re
from pathlib import PurePath, Path
from textblob_de import TextBlobDE

"""
new search
"""

class searchText:
    def __init__(self, keyword, folder2parse, extension="*.transcript"):
        self.extension = extension
        self.folder2parse = Path(folder2parse)
        self.list_all_texts = []
        self.all_text_files()
        self.keyword = keyword
        self.numberOfMentions = 0
        self.keywordPositions = 0
        self.list_keywords = []
        self.list_sentences = []
        self.search4keyword()
        self.getSentences()

        #print(self.occurrences)
    #def get_vid_id(self):

    def getSentences(self):
        for key in self.list_keywords:
            with open(*key, "r") as f:
                data = f.read()
            blob = TextBlobDE(data)
            counter = 0
            for sentence in blob.sentences:
                if self.keyword in sentence:
                    #print("_"*80)
                    #print("<3"*40)
                    id = str(*key)[-23:-11]
                    #print("sentence with keyword: " )
                    self.list_sentences.append({"index":counter, "id":id, "result":str(sentence)})
                    counter += 1
                    #print("_"*80)
                    #print("<3"*40)

    def all_text_files(self):
        all_text_files = []
        for file in self.folder2parse.glob(self.extension):
            all_text_files.append(file)
        self.list_all_texts = all_text_files

    def search4keyword(self):
        numberOfMentions = 0
        #list_starts_files
        list_keywords = []
        for text in self.list_all_texts:
            with open(text, "r") as f:
                data = f.read()
            startKeyword = data.find(self.keyword, 0)
            if startKeyword != -1:
                numberOfMentions += 1
            positions = [m.start() for m in re.finditer(self.keyword, data)]
            if positions != []:
                list_keywords.append({text: positions})
        self.numberOfMentions = numberOfMentions
        self.list_keywords = list_keywords


if __name__ == "__main__":
    folder2parse = r"\\DATEN\Schöpferwissen\UBC TV"
    #extension is set to "-transcript" by default
    search = searchText("hallo", folder2parse)
