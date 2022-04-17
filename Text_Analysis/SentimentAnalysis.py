from textblob_de import TextBlobDE as TextBlob
import os, glob
import pandas as pd

"""
Klasse die Sentimentwerte einem DF zuordnet
zwei Argumente:  Ornder mit Trnacribt Dateien /  Folder wo csv dateien drin sind
"""

folder_CSVs = r"C:\Users\Stacky\Desktop\HottisExperimentalcode\Text_Analysis\DATA\Channel_CSVs"

class Sentiment2CSV:
    def __init__(self, folder_with_transcripts, folder_with_DFs):
        self.folder_with_trans = folder_with_transcripts
        self.folder_with_DFs = folder_with_DFs
        self.all_transcript = glob.glob(self.folder_with_trans + "\*.transcript")
        self.list_all_CSVs = []
        self.All_CSVs()
        self.newDF = pd.DataFrame(columns=["id", "polarity", "sensivity"])
        self.get_all_sentiments()
        self.MergeDfs()

    def getSentiment(self, filename):
        with open(filename, "r") as f:
            text = str(f.readlines())
        blob = TextBlob(text)
        return blob.sentiment

    def get_all_sentiments(self):
        df = pd.DataFrame()
        id = ""
        for transcript in self.all_transcript:
            id = os.path.splitext(transcript)[0]
            id = id[-11:]
            newsent =  self.getSentiment(transcript)
            df= df.append({"id": id,"polarity": newsent[0], "subjectivity": newsent[1]}, ignore_index=True)
        df.to_csv(("BUBTEST.csv"))
        self.newDF = df

    def All_CSVs(self):
        ending = "*.csv"
        all_csv_files = []
        for path, subdir, files in os.walk("."):
            for file in glob.glob(os.path.join(path, ending)):
                all_csv_files.append(file)
        self.list_all_CSVs = all_csv_files

    def MergeDfs(self):
        counter = 0
        for csv in self.list_all_CSVs:
            df = pd.read_csv(csv)
            try:
                df_merge = df.merge(self.newDF, how="left", on="id")
                test = csv.split("\\")[-1]
                print(test)
                df_merge.to_csv(test)
            except:
                print("*"*50)
                print("Hello! didnt work with: " + str(csv))
                print("*"*50)

            #df.loc[df['first_name'] == 'Bill', 'Sentiment'] = 'Match'

folder_CSVs = r"D:\User\Documents\!code\schoepferwissen\DATA\Channel_CSVs"
folder_trans = "DATA"
sent = Sentiment2CSV(folder_trans, folder_CSVs)
