from addDict2Df import addDict2Df
from metadata import get_video_info
from addDict2Df import addDict2Df
from pytube import Channel 
import pandas as pd


#beispiel
channel_url= 'https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos'

df = pd.DataFrame()
channel = Channel(channel_url)
counter = 0
for url in channel.video_urls:
    counter = counter +1
    print('Download metadata ' + str(counter) + ' of ' + str(len(channel.video_urls)))
    print(url)
    dict_video = get_video_info(url)
    df = addDict2Df(dict_video)
print(df)
filename = "SchöpferwissenTV"+".csv"
df.to_csv(filename, index=False)


