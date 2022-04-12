import os
import glob
from SentimentAnalysis import getSentiment
from wordCloud import wordcloud
import pandas as pd

directory = glob.glob("DATA/*.transcript")
nichtinteressant = "eine aus dem des wenn ich Menschen und von Der das den wir ist die auf im"
PNG_names = pd.DataFrame
for filename in directory:
    
    wordcloud(filename, nichtinteressant, show = False)
    Sentiment = getSentiment(filename)
    print(Sentiment)
