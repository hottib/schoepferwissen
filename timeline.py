import streamlit as st
from streamlit_timeline import timeline
import pandas as pd
from pathlib import Path, PurePath
import base64

basefolder = r"\\DATEN\Schöpferwissen\.DATA"
datajson = basefolder + r"\timeline.json"
images = ["marc-unfall.png"]

#if we don't find above path, ask for a new one
while not Path(datajson).exists():
    with st.form('data_form'):
        newfolder = st.text_input('Data-Verzeichnis eingeben (ohne Slash am Ende):', '')
        newjson = newfolder + r"\timeline.json"
        submitted = st.form_submit_button("OK")
        if not newfolder:
            st.stop()
        elif not Path(newjson).exists():
            st.write('eingegebenen Pfad nicht gefunden')
            newfolder = None
            st.stop()
        else:
            datajson = newjson

# use full page width
st.set_page_config(page_title="Timeline Example", layout="wide")

# load data
with open(datajson, encoding='utf-8', mode="r") as f:
    timelinedata = f.read()

#since streamlit has no easy solution for serving static files, we manually put our images into the local static folder and reference them in a list
for imagename in images.items():
    timelinedata = timelinedata.replace(imagename, f"./static/timeline-media/{imagename}")


# render timeline
timeline(timelinedata, height=800)
