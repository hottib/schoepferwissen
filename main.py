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
        channel_name = ''.join(c for c in channel.channel_name if c not in '?')
        basefolder = r"K:\Schoepferwissen\.DATA"
        filename = os.path.join(basefolder, channel_name + "_manuell.csv")

        if os.path.exists(filename):
            print(f'{filename} already exists. Skipping.')
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
        features = ["publish_date", "id", "title", "description", "keywords", "length", "views", "age_restricted", "yt_caption_info", "yt_caption_tracks", "vid_info"]
        new_row = [0] * len(features)

        channel = Channel(self.channel_url)
        channel_name = ''.join(c for c in channel.channel_name if c not in '?')
        idlist = [url.replace("https://www.youtube.com/watch?v=", "") for url in channel.video_urls]
        basefolder = r"K:\Schoepferwissen\.DATA"
        filename = os.path.join(basefolder, channel_name + "_automated.csv")
        filebakname = os.path.join(filename + ".bak")

        if not os.path.exists(filename):
            if os.path.exists(filebakname):
                print(f'{filename} not found. Restoring backup.')
                os.rename(filebakname, filename)
            else:
                df = pd.DataFrame(columns=features)
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            for id in df["id"]:
                if id in idlist:
                    idlist.remove(id)
            if len(idlist) > 0:
                print(f'Found new videos for {filename}. Creating backup.')
                if os.path.exists(filebakname):
                    os.remove(filebakname)
                os.rename(filename, filebakname)
            else:
                print(f'No new videos for {filename}.')
                return

        print(f"Processing channel {channel_name} for metadata...")
        for id in idlist:
            yt = YouTube("https://www.youtube.com/watch?v="+id)
            yt.bypass_age_gate()
            yt.check_availability()
            publish_date = yt.publish_date
            video_id = id
            print(f"\r{video_id}", end="")
            title = yt.title
            description = yt.description
            tags = yt.keywords
            length = yt.length
            views= yt.views
            #seems to be outdated
            #metadata = yt.metadata
            age_restricted = yt.age_restricted
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
            df.loc[len(df.index)] = new_row
            df.to_csv(filename, index=False)
        print("\r"+"="*100)
        print("Saved as:", filename)
        print("="*100)
        df.to_csv(filename, index=False)
            
if __name__ == '__main__':

    features =  ["id", "sentiments", "effects", "sound", "behaviour", "tags", "people", "location", "CDS"]

    #Hauptkanal "Schöpferwissen TV"
    #Schoepf_channel_url="https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos"

    #Nebenkanal "Creator Monkeys TV", Mai 2017 - Mai 2022, Betreiber*in vermutlich Julia
    Monkeys_channel_url="https://www.youtube.com/@creatormonkeystv6514"

    #gelöschter Nebenkanal "Der Wahrheit verpflichtet"
    #Wahrheit_channel_url="https://www.youtube.com/c/DerWahrheitverpflichtet"
    #gelöschter Nebenkanal "Honett"
    #Honett_channel_url="https://www.youtube.com/channel/UC2BK1JGDSB0RFSJdijEBnpA"

    #Nebenkanal "Der Weg in deine Freiheit", Mai 2019 - August 2021, Betreiber vermutlich Heiko, mit Links zu seinen diversen Blogs
    Freiheit_channel_url= "https://www.youtube.com/@derwegindeinefreiheit9206/videos"

    #Kanal-System, betrieben von ? (nicht Tina)
    #Nebenkanal "WISSEN - NICHT VON DIESER WELT", gelöscht seit 22.3.23
    WISSEN_channel_url="https://www.youtube.com/@wissen-nichtvondieserwelt6328/videos"
    #Nebenkanal "Der verlorene Zwilling TV"
    Zwilling_channel_url="https://www.youtube.com/@derverlorenezwillingtv5818/videos"
    #Nebenkanal "ALLESUNDNICHTS"
    ALLES_channel_url="https://www.youtube.com/@allesundnichts6336/videos"
    #Nebenkanal "Drachentöter TV", gelöscht 31.3.2023
    Drachentoeter_channel_url="https://www.youtube.com/@drachentotertv1867/videos"
    #Nebenkanal "WER HAT ANGST VORM SCHWARZEN MANN"
    SCHWARZ_channel_url="https://www.youtube.com/@werhatangstvormschwarzenma4240/videos"
    #Nebenkanal "Veit Club"
    VEITCLUB_channel_url="https://www.youtube.com/@veitclub6907/videos"
    #Nebenkanal "SON GOKU TV"
    SONGOKU_channel_url="https://www.youtube.com/@songokutv8924/videos"
    #Nebenkanal "Rettung der Menschheit TV" / Rettung Menschheit UBC (Rettung der Menschheit mit dem Schwert des Wissens)
    #Es ist alles gesagt / Aus die Maus (geleert)
    #seit 21.3.2023 zurück als "Rettung Menschheit?" / "Rettung Menscheit UBC"
    Rettung_channel_url="https://www.youtube.com/@DasWissen/videos"


    #Nebenkanal-Netzwerk betrieben von "Wau Maumau"
    #Seiten: http://ausschn.de, https://www.facebook.com/wau.maumau.3, https://www.facebook.com/wau.maumau.33, https://www.instagram.com/ungeeignet/
    #Email: wau.maumau@gmail.com, plusminusmore@gmail.com
    #eventuell Anka Görke-Fährmann https://www.facebook.com/bebe.bremerbutjer / https://www.facebook.com/HandKunst
    #Nebenkanal "u n endlich / guelty till 11.12.23", viele gelöscht
    unendlich_channel_url="https://www.youtube.com/@_00Oq_____pO00/videos"
    #Nebenkanal "___________k______ungefähr"
    ungefaehr_channel_url="https://www.youtube.com/@_________F--A------EHR/videos"

    #Nebenkanal "PLANET VEIT", April 2022, Betreiber*in vermutlich ebenfalls wie oben
    PLANET_channel_url="https://www.youtube.com/@planetveit8902/videos"

    #Kanal "veritas lügensarg tv", Betreiber*in Gelgia? (Location Schweiz)
    veritas_channel_url="https://www.youtube.com/@veritaslugensargtv8637/videos"

    #Steffis Kanal: "Schöpferwissen TV UBC (ehemals Verloren und Wiedergefunden), nach Thomas Entlassung alte SW-Videos gelöscht"
    Verloren_channel_url="https://www.youtube.com/@verlorenundwiedergefunden4330/videos"
    #Tinas Kanal: Schöpferwissen TV TIME FOR JUSTICE UBC, jetzt Schöpferwissen TV UBC NOBODY KNOWS
    Justice_channel_url="https://www.youtube.com/@timeforjusticeTV/videos"

    #Nebenkanal "UBC TV", Mai-Juni 2017, Betreiber*in unklar
    UBC_channel_url="https://www.youtube.com/@ubctv9741/videos"
    #Nebenkanal "Schöpferwissen- Peek-TV", März-Oktober 2017, Betreiber*in unklar
    Peek_channel_url="https://www.youtube.com/@schopferwissen-peek-tv3821/videos"
    #Nebenkanal "The time is now", Mai-Juni 2018, Betreiber*in unklar
    TheTime_channel_url="https://www.youtube.com/@thetimeisnow9902/videos"
    #Nebenkanal "bewusstundso", Juli 2017 - Juni 2019, Betreiber*in unklar
    bewusstundso_channel_url="https://www.youtube.com/@bewusstundso9618/videos"

    #Nebenkanal "Schöpferwissen TV - Backup NEU (siehe Kanalinfo)", , Betreiber*in ?
    backupneu_channel_url="https://www.youtube.com/@schopferwissentv-backupneu2752/videos"


    try:
        collect_channel_data = CollectChannelData(Schoepf_channel_url, basefolder= "DATA")
        collect_channel_data.process_channel()
            #collect_channel_data.create_empty_csv(features)
    except:
        print(item +" hat nicht geklappt")



    all_channels = [
        #Schoepf_channel_url,
        #Wahrheit_channel_url,
        Rettung_channel_url,
        Freiheit_channel_url,
        ALLES_channel_url,
        VEITCLUB_channel_url,
        #Drachentoeter_channel_url,
        UBC_channel_url,
        unendlich_channel_url,
        #Honett_channel_url,
        #WISSEN_channel_url,
        Zwilling_channel_url,
        SONGOKU_channel_url,
        PLANET_channel_url,
        SCHWARZ_channel_url,
        veritas_channel_url,
        Peek_channel_url,
        Verloren_channel_url,
        TheTime_channel_url,
        Justice_channel_url,
        bewusstundso_channel_url,
        ungefaehr_channel_url,
        Monkeys_channel_url,
        backupneu_channel_url
    ]

    #EINE CSV ERSTELLEN
    #collect_channel_data = CollectChannelData(VEITCLUB_channel_url)
    #collect_channel_data.update("DATA")


    #Multiple CSVs erstellen


    for item in all_channels:
#        try:
        collect_channel_data = CollectChannelData(item)
        collect_channel_data.process_channel()
        collect_channel_data.create_empty_csv(features)
#        except:
#            print(item +" hat nicht geklappt")
    print("FERTIG")
