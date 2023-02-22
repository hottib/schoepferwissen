# change Channel.py to https://github.com/pishiko/pytube/blob/fix-channel/pytube/contrib/channel.py
from pytube import Channel, YouTube
import pandas as pd
import os, glob

class CollectChannelData: 
    
    def __init__(self, channel_url, basefolder = r"C:\Users\Stacky\Desktop\schöpferwissen_code\schoepferwissen", list_of_all_channels = []):
        self.channel_url = channel_url
        self.all_channels= all_channels
        self.basefolder = basefolder

    def update(self, folderWithCSVs):
        all_CSVs = glob.glob(folderWithCSVs +"\*_automated.csv")
        
        for csv in all_CSVs: 
            print("Checking %s ..." %csv)
            self.update_counter = 0
            df = pd.read_csv(csv)
            if not df.empty:
                df_sort = df.sort_values("publish_date", ascending = False)
                lastupdate = df_sort.at[0, "publish_date"]
                lastupdate = self.Date2int(lastupdate)  
            else:
                print("csv is empty calling process channel") 
            
            for channel_url in self.all_channels:
                channel = Channel(channel_url)
                channel_name = channel.channel_name
                csvClean = csv.replace(self.basefolder,"").replace("_automated.csv", "")
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
                        print("I"*70)
                        print("Updating "+ channel_url)
                        print("Channel URL "+ channel_url)
                        print("Channel ID  " + channel.channel_id)
                        print("Channel Name  " + channel_name)
                        print(f"csvCLean is: {csvClean}")
            print("There are %s new Vids" % self.update_counter)
                        
    def Date2int(self, date):
        integer = date.replace("-", "")
        integer = int(integer)
        return integer          

    def process_channel(self):
        df = pd.DataFrame()
        channel = Channel(self.channel_url)
        channel_name = channel.channel_name
        filename = os.path.join(self.basefolder, channel_name + "_automated.csv")
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
            #print(f"\r{video_id}", end="")
            title = yt.title
            description = yt.description
            tags = yt.keywords
            length = yt.length
            views= yt.views
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
            #print(new_row)
            df.loc[len(df.index)]= new_row
        if channel.video_urls != []:
            print("\r"+"="*100)
            print(self.basefolder)
            print("Saved as:", filename)
            print("="*100)
            df.to_csv(filename, index=False)
        else : print(f"No Vids found under {channek}")
                
if __name__ == '__main__':

    features =  ["publish_date","id", "title", "sentiments", "effects", "sound", "behaviour", "tags", "people", "location"]
    #DIESe Kanäle gibt es nicht mehr
    #Hauptkanal "Schöpferwissen TV": 938 Videos
    Schoepf_channel_url="https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos"
    #Nebenkanal "Der Wahrheit verpflichtet": 994 Videos
    Wahrheit_channel_url="https://www.youtube.com/c/DerWahrheitverpflichtet"
    #Nebenkanal "Honett"
    Honett_channel_url="https://www.youtube.com/channel/UC2BK1JGDSB0RFSJdijEBnpA"
    
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
    #Nebenkanal "WISSEN - NICHT VON DIESER WELT"
    WISSEN_channel_url="https://www.youtube.com/channel/UC5Sr_xoXTkBThtqthLwOkPg"
    #Nebenkanal "Der verlorene Zwilling TV"
    Zwilling_channel_url="https://www.youtube.com/channel/UCMCVs7vtSk2aTLDaGUkHQYQ"
    #Nebenkanal "PLANET VEIT"
    PLANET_channel_url="https://www.youtube.com/channel/UC0KvN280Qjkh4Albvhibt1A"
    #Nebenkanal "WER HAT ANGST VORM SCHWARZEN MANN"
    SCHWARZ_channel_url="https://www.youtube.com/channel/UCa7jxqU8qeHABn_Y4-GE1Uw"
    #Neuer Kanal 6 Monate alt
    yt = YouTube("https://www.youtube.com/watch?v=Sa8lt2Dk2KI&t=126s")
    c = yt.channel_url
    SCHOEPF_TV_UBC_url =c
    #Leere Kanal ??? Y Julia?
    DAS_WISSEN_url = "https://www.youtube.com/@DasWissen/"
    
    folder = r"schoepferwissen\DATA"
    
    all_channels = [
        SCHOEPF_TV_UBC_url,
        Rettung_channel_url,
        Freiheit_channel_url,
        ALLES_channel_url,
        VEITCLUB_channel_url,
        Drachentoeter_channel_url,
        UBC_channel_url,
        unendlich_channel_url,
        WISSEN_channel_url,
        Zwilling_channel_url,
        PLANET_channel_url,
        SCHWARZ_channel_url
    ]

    #EINE CSV ERSTELLEN
    #collect_channel_data = CollectChannelData(VEITCLUB_channel_url)
    #collect_channel_data.update("DATA")


    #Multiple CSVs erstellen
    #update = CollectChannelData(WISSEN_channel_url, basefolder= r"schoepferwissen\Test")
    #update.update(r"schoepferwissen\Test")

    #url = "https://www.youtube.com/channel/UCWELnCGV_IYWctpTPiB8-Sw"
    #collect_channel_data = CollectChannelData(url, basefolder= r"schoepferwissen\Test")
    #collect_channel_data.process_channel()
   
    for item in all_channels:
        try:
            collect_channel_data = CollectChannelData(item, basefolder= folder)
            collect_channel_data.process_channel()
            #collect_channel_data.create_empty_csv(features)
        except:

            print(item +" hat nicht geklappt")


    #Welche Videos wurden gelöscht?
    #Vllt noch in den MEtadaten bisschen rumwühlen

