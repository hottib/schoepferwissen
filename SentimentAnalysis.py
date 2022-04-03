from googletrans import Translator
from textblob_de import TextBlobDE as TextBlob
import pandas as pd
import re
data = pd.read_csv("Der Weg in deine Freiheit.csv")

#print(data['transcript'][2])


text= data.transcript[1]

text= str(text)
D2=eval(text)
print(D2)

text= text.replace("[{'text': ", '').replace("'start': ", "").replace("[Musik]", "")
text= text.replace("duration", "").replace("'", "").replace(",", "").replace(":", "")
pattern = r'[0-9]'
# Match all digits in the string and replace them with an empty string
text = re.sub(pattern, '', text)
print(text)

blob = TextBlob(text)
print(blob.sentiment)