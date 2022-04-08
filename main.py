from pytube import Channel, YouTube
import pandas as pd

class CollectChannelData: 
    def __init__(self, channel_url):
        self.hello = "HELLO"

    def create_empty_csv(self, featrues):
        #TODO: Excetion handeln.... csv File überschreiben.....
 
        channel = Channel(channel_url)
        channel_name = channel.channel_name
        filename= "DATA/"+ channel_name + "_manuel.csv"
        try:
            df = pd.DataFrame(filename)
        except:
            df = pd.DataFrame(columns=featrues)
            listofzeros = [0] * len(featrues)
            for url in channel.video_urls:
                id = url.replace("https://www.youtube.com/watch?v=", "")
                print(id)
                yt = YouTube(url)
                title = yt.title
                date = yt.publish_date
                new_row = listofzeros
                new_row[0] = date
                new_row[1] = id
                new_row[2] = title
                df.loc[len(df.index)]= new_row
            df.to_csv(filename, index=False)
            print("NEW Filename: " + filename)


    def process_channel(self):
        #TODO: Excetion handeln.... csv File überschreiben.....

        df = pd.DataFrame()
        channel = Channel(channel_url)
        channel_name = channel.channel_name
        filename= "DATA/"+ channel_name + "_automated.csv"
        features = ["publish_date", "id", "title", "description", "keywords", "length", "views", "age_restricted", "yt_caption_info", "yt_caption_tracks", "vid_info"]
        df = pd.DataFrame(columns=features)
        new_row = [0] * len(features)
        for url in channel.video_urls:
            yt = YouTube(url)
            yt.bypass_age_gate()
            yt.check_availability()
            
            publish_date = yt.publish_date
            id = url.replace("https://www.youtube.com/watch?v=", "")
            title = yt.title
            description = yt.description
            tags = yt.keywords
            length = yt.length
            views= yt.views
            #seems to be outdated
            #metadata = yt.metadata
            age_restricted= yt.age_restricted
            yt_caption_info = yt.captions
            vid_info = yt.vid_info
            new_row[0] = publish_date
            new_row[1] = id
            new_row[2] = title
            new_row[3] = description
            new_row[4] = tags
            new_row[5] = length
            new_row[6] = views
            new_row[7] = age_restricted
            new_row[8] = yt_caption_info
            new_row[9] = vid_info
            df.loc[len(df.index)]= new_row
        print("="*100)
        print("Saved as:" + filename)
        print("="*100)
        df.to_csv(filename, index=False)
            
if __name__ == '__main__':

    features =  ["publish_date","id", "title", "sentiments", "effects", "sound", "behaviour", "tags", "people", "location"]
    #HIER KANAL AUSWÄHLEN
    #Hauptkanal "Schöpferwissen TV": 938 Videos
    channel_url="https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos"
    #Nebenkanal "Der Wahrheit verpflichtet": 994 Videos
    channel_url="https://www.youtube.com/c/DerWahrheitverpflichtet"
    #Nebenkanal "Rettung der Menschheit TV": 92 Videos
    channel_url="https://www.youtube.com/channel/UC5ZGCLwrKIJrdhYwHYcXCvA/videos"
    #Nebenkanal "Der Weg in deine Freiheit": 32 Videos
    channel_url= "https://www.youtube.com/channel/UCysE7uKxMA9g7u_6Zzf2iKQ/videos"
    #Nebenkanal "ALLESUNDNICHTS": 48 Videos
    channel_url="https://www.youtube.com/channel/UCewNpvf2bcJVaXju9r_EOxw/videos"
    #Nebenkanal "Veit Club": 17 Videos
    channel_url="https://www.youtube.com/channel/UCzlH19qwncW1Th9z3tWIeKQ/videos"
    #Nebenkanal "Drachentöter TV": 287 Videos
    channel_url="https://www.youtube.com/channel/UC4StsLMnfcOuQ374_oGa5sg/videos"
    #Nebenkanal "UBC TV": 11 Videos
    channel_url="https://www.youtube.com/channel/UCWELnCGV_IYWctpTPiB8-Sw"
    collect_channel_data = CollectChannelData(channel_url)
    collect_channel_data.process_channel()
    #collect_channel_data.create_empty_csv(features)
    #print(collect_channel_data.hello)
    #collect_channel_data.process_channel(channel_url)
