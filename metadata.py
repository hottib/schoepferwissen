import pandas
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import re
import json
from getplaylist import channel
import csv
import pandas as pd
# init session
session = HTMLSession()
 

def get_video_info(url):
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(timeout=60)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    # open("index.html", "w").write(response.html.html)
    # initialize the result
    result = {}
    df = pd.DataFrame()
    # video title
    result["title"] = soup.find("meta", itemprop="name")['content']
    # video views
    result["views"] = soup.find("meta", itemprop="interactionCount")['content']
    # video description
    result["description"] = soup.find("meta", itemprop="description")['content']
    print(result["description"])
    # date published
    result["date_published"] = soup.find("meta", itemprop="datePublished")['content']
    # get the duration of the video
    result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text
    # get the video tags
    result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
    
    return result
    
 


if __name__ == "__main__":
    #channel('https://www.youtube.com/channel/UCGQFj8C3sMhxuFJjkANkyKA/videos')
    url= "https://www.youtube.com/watch?v=YL9ZvwHDAXQ"
    
    data = get_video_info(url)

    # print in nice format
    
    print(f"Title: {data['title']}")
    print(f"Views: {data['views']}")
    print(f"Published at: {data['date_published']}")
    print(f"Video Duration: {data['duration']}")
    print(f"Video tags: {data['tags']}")
    print(f"Likes: {data['likes']}")
    print(f"Dislikes: {data['dislikes']}")
    print(f"\nDescription: {data['description']}\n")
    print(f"\nChannel Name: {data['channel']['name']}")
    print(f"Channel URL: {data['channel']['url']}")
    print(f"Channel Subscribers: {data['channel']['subscribers']}")

   # for keys, values in data.items():
    #    print(keys)
     #   print(values)
    df = pd.DataFrame.from_dict(data)
    print(df)
    df.to_csv('out.csv')