from pytube import Channel 
import csv
      
def channel(channel_url): 
    with open('new_names.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file , dialect='excel', delimiter = ",")
        c = Channel(channel_url)
        for url in c.video_urls:
            csv_writer.writerow([url])

#DEMO        
channel('https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos')