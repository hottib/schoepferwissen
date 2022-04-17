import os, glob, re
from textblob_de import TextBlobDE

"""
new search
"""

class searchText:
    def __init__(self, keyword, folder2parse, extension="*.transcript"):
        self.extension = extension
        self.folder2parse = folder2parse
        self.list_all_texts = []
        self.all_text_files()
        self.keyword = keyword
        print(type(self.list_all_texts))

        self.numberOfMentions = 0
        self.keywordPositions = 0
        self.list_keywords = []
        self.search4keyword()
        self.getSentences()

        #print(self.occurrences)
    #def get_vid_id(self):
    def getSentences(self):
        for key in self.list_keywords:
            with open(key[0], "r") as f:
                data = f.read()
            blob = TextBlobDE(data)
            for sentence in blob.sentences:
                if self.keyword in sentence:
                    print("_"*80)
                    print("<3"*40)
                    id = key[0][-23:-11]
                    print("Find keyword in: " + id)
                    print("sentence with keyword: " )
                    print(sentence)
                    print("_"*80)
                    print("<3"*40)


    def all_text_files(self):
        all_text_files = []
        for path, subdir, files in os.walk(self.folder2parse):
            search_path = os.path.join(path, self.extension)
            for file in glob.glob(search_path):
                all_text_files.append(file)
        self.list_all_texts = all_text_files

    def search4keyword(self):
        numberOfMentions = 0
        #list_starts_files
        list_keywords = []
        for text in self.list_all_texts:
            with open(text, "r") as f:
                data = f.read()
            startKeyword =data.find(self.keyword, 0)
            if startKeyword != -1:
                numberOfMentions += 1
            positions = [m.start() for m in re.finditer(self.keyword, data)]
            if positions != []:
                list_keywords.append([text, positions])
        self.numberOfMentions = numberOfMentions
        self.list_keywords = list_keywords





if __name__ == "__main__":
    folder2parse = "."
    #extension is set to "-transcript" by default
    search = searchText("Corona", folder2parse)
