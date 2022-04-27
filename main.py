from pytube import Channel, YouTube
import pandas as pd
import os, glob

class CollectChannelData: 
    

    
    def __init__(self, channel_url, basefolder = r"\\DATEN\Schöpferwissen\.DATA"):
        self.hello = "HELLO"
        self.channel_url = channel_url
            #Hauptkanal "Schöpferwissen TV": 938 Videos
        Schoepf_channel_url="https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos"
        #Nebenkanal "Der Wahrheit verpflichtet": 994 Videos
        Warheit_channel_url="https://www.youtube.com/c/DerWahrheitverpflichtet"
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
        #EINE CSV ERSTELLEN
        self.all_channels= [
        Rettung_channel_url,
        Schoepf_channel_url, 
        Warheit_channel_url,  
        Freiheit_channel_url, 
        ALLES_channel_url,
        VEITCLUB_channel_url,
        Drachentoeter_channel_url,
        UBC_channel_url
        ]
        self.basefolder = basefolder

    def update(self, folderWithCSVs):
        channel = Channel(self.channel_url)
        
        all_CSVs = glob.glob(folderWithCSVs +"\*_automated.csv")
        for csv in all_CSVs: 
            #print(csv)
            self.update_counter = 0
            df = pd.read_csv(csv)
            df_sort = df.sort_values("publish_date", ascending = False)
            lastupdate = df_sort.at[0, "publish_date"]
            lastupdate = self.Date2int(lastupdate)
            print("Checking %s ..." %csv)
            for channel_url in self.all_channels:
                channel = Channel(channel_url)
                channel_name = channel.channel_name
                csvClean = csv.replace("DATA\\","").replace("_automated.csv", "")
                
                if channel_name == csvClean:
                    for url in channel.video_urls:
                        yt = YouTube(url)
                        yt_date = yt.publish_date
                        yt_date =str(yt_date)[:10]     
                        yt_date_conv = self.Date2int(yt_date)
                        if yt_date_conv > lastupdate:
                            self.update_counter += 1
                            id = url.replace("https://www.youtube.com/watch?v=", "")
                            title = yt.title
                            description = yt.description
                            tags = yt.keywords
                            length = yt.length
                            views= yt.views
                            age_restricted= yt.age_restricted
                            yt_caption_info = yt.captions
                            vid_info = yt.vid_info
                            data = []
                            data.insert(0, {"publish_date": yt_date, 
                                            "id": id, 
                                            "title": title, 
                                            "description": description, 
                                            "keywords": tags, 
                                            "length": length, 
                                            "views": views, 
                                            "age_restricted": age_restricted, 
                                            "yt_caption_info": yt_caption_info})
                            updated_df = pd.concat([pd.DataFrame(data), df], ignore_index=True)
                            updated_df.to_csv(csv)
                        else: 
                            break
            print("There are %s new Vids" % self.update_counter)
                        
    def Date2int(self, date):
        integer = date.replace("-", "")
        integer = int(integer)
        return integer
            
            
    def create_empty_csv(self, featrues):   
        channel = Channel(self.channel_url)
        channel_name = channel.channel_name
        filename= "DATA/"+ channel_name + "_manuel.csv"
        try:
            df = pd.DataFrame(filename)
            print("File already exists. Use self.update for adding")
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
        channel_name = channel.channel_name
        filename= "../DATA/"+ channel_name + "_manuell.csv"
        try:
            print(filename)
            df = pd.read_csv(filename)
            print(df)

            print("Update NOW!")

        except:
            print(filename)



    def create_empty_csv(self, features):
        channel = Channel(self.channel_url)
        channel_name = channel.channel_name
        filename = os.path.join(self.basefolder, channel_name + "_manuell.csv")
        if os.path.exists(filename):
            print(f'File {filename} already exists. Skipping.')
            return

        df = pd.DataFrame(columns=features)
        listofblanks = [' '] * len(features)
        print(f"Processing manual CSV for channel {channel_name}...")
        for url in channel.video_urls:
            video_id = url.replace("https://www.youtube.com/watch?v=", "")
            print(f"\r{video_id}", end="")
            new_row = listofblanks
            new_row[0] = video_id
            df.loc[len(df.index)]= new_row
        df.to_csv(filename, index=False)
        print("\r"+"="*100)
        print("Saved as:", filename)
        print("="*100)


    def process_channel(self):
        df = pd.DataFrame()
        channel = Channel(self.channel_url)
        channel_name = channel.channel_name
        filename = os.path.join(basefolder, channel_name + "_automated.csv")

        if os.path.exists(filename):
            print(f'File {filename} already exists. Skipping.')
            return

        features = ["publish_date", "id", "title", "description", "keywords", "length", "views", "age_restricted", "yt_caption_info", "yt_caption_tracks", "vid_info"]
        df = pd.DataFrame(columns=features)
        new_row = [0] * len(features)
        print(f"Processing channel {channel_name} for metadata...")
        for url in channel.video_urls:
            yt = YouTube(url)
            yt.bypass_age_gate()
            yt.check_availability()
            publish_date = yt.publish_date
            video_id = url.replace("https://www.youtube.com/watch?v=", "")
            print(f"\r{video_id}", end="")
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
            new_row[1] = video_id
            new_row[2] = title
            new_row[3] = description
            new_row[4] = tags
            new_row[5] = length
            new_row[6] = views
            new_row[7] = age_restricted
            new_row[8] = yt_caption_info
            new_row[9] = vid_info
            df.loc[len(df.index)]= new_row
        print("\r"+"="*100)
        print("Saved as:", filename)
        print("="*100)
        df.to_csv(filename, index=False)
            
if __name__ == '__main__':

    features =  ["publish_date","id", "title", "sentiments", "effects", "sound", "behaviour", "tags", "people", "location"]
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
    #Nebenkanal "u n endlich"
    unendlich_channel_url="https://www.youtube.com/channel/UCyIj6T2W5xQsi7dCbfuJdUw"
    #Nebenkanal "Honett"
    Honett_channel_url="https://www.youtube.com/channel/UC2BK1JGDSB0RFSJdijEBnpA"
    #Nebenkanal "WISSEN - NICHT VON DIESER WELT"
    WISSEN_channel_url="https://www.youtube.com/channel/UC5Sr_xoXTkBThtqthLwOkPg"
    #Nebenkanal "Der verlorene Zwilling TV"
    Zwilling_channel_url="https://www.youtube.com/channel/UCMCVs7vtSk2aTLDaGUkHQYQ"
    #Nebenkanal "PLANET VEIT"
    PLANET_channel_url="https://www.youtube.com/channel/UC0KvN280Qjkh4Albvhibt1A"
    #Nebenkanal "WER HAT ANGST VORM SCHWARZEN MANN"
    SCHWARZ_channel_url="https://www.youtube.com/channel/UCa7jxqU8qeHABn_Y4-GE1Uw"

    all_channels = [
        Schoepf_channel_url,
        Wahrheit_channel_url,
        Rettung_channel_url,
        Freiheit_channel_url,
        ALLES_channel_url,
        VEITCLUB_channel_url,
        Drachentoeter_channel_url,
        UBC_channel_url,
        unendlich_channel_url,
        Honett_channel_url,
        WISSEN_channel_url,
        Zwilling_channel_url,
        PLANET_channel_url,
        SCHWARZ_channel_url
    ]

    #EINE CSV ERSTELLEN
    #collect_channel_data = CollectChannelData(VEITCLUB_channel_url)
    #collect_channel_data.update("DATA")


    #Multiple CSVs erstellen
    """"
    all_channels= [
    Schoepf_channel_url, 
    Warheit_channel_url, 
    Rettung_channel_url, 
    Freiheit_channel_url, 
    ALLES_channel_url,
    VEITCLUB_channel_url,
    Drachentoeter_channel_url,
    UBC_channel_url
    ]

    all_channels= [
    Rettung_channel_url, 
    Freiheit_channel_url, 
    ALLES_channel_url,
    VEITCLUB_channel_url,
    Drachentoeter_channel_url,
    UBC_channel_url
    ]
    """

    """
    for item in all_channels:
        collect_channel_data = CollectChannelData(item)
        collect_channel_data.process_channel()
        collect_channel_data.create_empty_csv(features)
    print("FERTIG HAT ALLES GEKLAPPT")
    
    #collect_channel_data.create_empty_csv(features)
    """
    for item in all_channels:
        try:
            collect_channel_data = CollectChannelData(item, basefolder= r"DATA")
            collect_channel_data.process_channel()
            #collect_channel_data.create_empty_csv(features)
        except:
            print(item +" hat nicht geklappt")
    print("FERTIG")
