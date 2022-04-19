from pytube import Channel, YouTube
import pandas as pd
import os

class CollectChannelData: 
    def __init__(self, channel_url):
        self.hello = "HELLO"
        self.channel_url = channel_url

    def update(self):
        channel = Channel(self.channel_url)
        channel_name = channel.channel_name
        filename= "../DATA/"+ channel_name + "_manuel.csv"
        try:
            print(filename)
            df = pd.read_csv(filename)
            print(df)

            print("Update NOW!")

        except:
            print(filename)



    def create_empty_csv(self, features):
        #TODO: Excetion handeln.... csv File überschreiben.....
 
        channel = Channel(self.channel_url)
        channel_name = channel.channel_name
        basefolder = r"\\DATEN\Schöpferwissen\.DATA"
        filename = os.path.join(basefolder, channel_name + "_manuell.csv")
        try:
            df = pd.DataFrame(filename)
            print("File already exists. Use self.update for adding")
        except:
            df = pd.DataFrame(columns=features)
            listofblanks = [' '] * len(features)
            for url in channel.video_urls:
                video_id = url.replace("https://www.youtube.com/watch?v=", "")
                print(video_id)
                new_row = listofblanks
                new_row[0] = video_id
                df.loc[len(df.index)]= new_row
            df.to_csv(filename, index=False)
            print("NEW Filename: " + filename)


    def process_channel(self):
        #TODO: Excetion handeln.... csv File überschreiben.....

        df = pd.DataFrame()
        channel = Channel(self.channel_url)
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

    features =  ["id", "sentiments", "effects", "sound", "behaviour", "tags", "people", "location", "CDS"]
    #HIER KANAL AUSWÄHLEN
    #Hauptkanal "Schöpferwissen TV": 938 Videos
    Schoepf_channel_url="https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos"
    #Nebenkanal "Der Wahrheit verpflichtet": 994 Videos
    Wahrheit_channel_url="https://www.youtube.com/c/DerWahrheitverpflichtet"
    #Nebenkanal "Rettung der Menschheit TV": 92 Videos
    Rettung_channel_url="https://www.youtube.com/channel/UC5ZGCLwrKIJrdhYwHYcXCvA/videos"
    #Nebenkanal "Der Weg in deine Freiheit": 32 Videos
    Freiheit_channel_url= "https://www.youtube.com/channel/UCysE7uKxMA9g7u_6Zzf2iKQ/videos"
    #Nebenkanal "ALLESUNDNICHTS": 48 Videos
    ALLES_channel_url="https://www.youtube.com/channel/UCewNpvf2bcJVaXju9r_EOxw/videos"
    #Nebenkanal "Veit Club": 17 Videos
    VEITCLUB_channel_url="https://www.youtube.com/channel/UCzlH19qwncW1Th9z3tWIeKQ/videos"
    #Nebenkanal "Drachentöter TV": 287 Videos
    Drachentoeter_channel_url="https://www.youtube.com/channel/UC4StsLMnfcOuQ374_oGa5sg/videos"
    #Nebenkanal "UBC TV": 11 Videos
    UBC_channel_url="https://www.youtube.com/channel/UCWELnCGV_IYWctpTPiB8-Sw"
    all_channels = [
        Schoepf_channel_url,
        Wahrheit_channel_url,
        Rettung_channel_url,
        Freiheit_channel_url,
        ALLES_channel_url,
        VEITCLUB_channel_url,
        Drachentoeter_channel_url,
        UBC_channel_url
    ]

    #EINE CSV ERSTELLEN
    #collect_channel_data = CollectChannelData(VEITCLUB_channel_url)
    #collect_channel_data.update()

    #Multiple CSVs erstellen
    for item in all_channels:
        try:
            collect_channel_data = CollectChannelData(item)
            collect_channel_data.process_channel()
            #collect_channel_data.create_empty_csv(features)
        except:
            print(item +" hat nicht geklappt")
    print("FERTIG HAT ALLES GEKLAPPT")
