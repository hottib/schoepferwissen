import streamlit as st
import pandas as pd
from pathlib import Path, PurePath
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from ast import literal_eval
from collections import ChainMap
import os, glob, re, numpy
import Text_Analysis.searchText as ft_search

#don't remember what this was for :D
def find_channel(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def convert_time(seconds):
    timehour = int(int(seconds) // 3600)
    timemin = int(int(seconds) // 60)
    timemin2 = int(timemin % 60)
    timesek = int(int(seconds) % 60)
    if timemin > 240:
        converted = f"{timehour:02d}:{timemin2:02d}:{timesek:02d}"
    else:
        converted = f"{timemin:02d}:{timesek:02d}"
    return converted

def cleanup_tags(tag_string):
    new_string = ''
    tag_list = literal_eval(tag_string)
    new_string = ', '.join([i for i in tag_list])
    return new_string

#define aggrid styling
grid_options = {
    "defaultColDef": {
        "resizable": True,
        "sortable": True,
        "editable": True,
    },
    "columnDefs": [
        {
            "headerName": 'automatisch',
            "children": [
                {
                    "headerName": "Datum",
                    "field": "publish_date",
                    "width": 250,

                },
                {
                    "headerName": "ID",
                    "field": "id",
                    "width": 250,
                },
                {
                    "headerName": "archiv.",
                    "field": "platform",
                    "width": 100,
                },
                {
                    "headerName": "Titel",
                    "field": "title",
                    "width": 800,
                },
                {
                    "headerName": "Beschreibung",
                    "field": "description",
                    "width": 600,
                },
                {
                    "headerName": "Länge",
                    "field": "length",
                    "width": 160,
                },
                {
                    "headerName": "Views",
                    "field": "views",
                    "width": 150,
                },
                {
                    "headerName": "YT-Tags",
                    "field": "keywords",
                },
                {
                    "headerName": "Sprache",
                    "field": "yt_caption_info",
                },
#                {
#                    "headerName": "18+",
#                    "field": "age_restricted",
#                },
            ]
        },
        {
            "headerName": 'manuell',
            "children": [
#                {
#                    "headerName": "sentiments",
#                    "field": "sentiments",
#                    "editable": True,
#                },
                {
                    "headerName": "Was",
                    "field": "behaviour",
                    "width": 600,
                },
                {
                    "headerName": "Wer",
                    "field": "people",
                },
                {
                    "headerName": "Wo",
                    "field": "location",
                },
                {
                    "headerName": "CDS",
                    "field": "CDS",
                    "cellEditor": "agSelectCellEditor",
                    "cellEditorParams": {
                        'values': [' ','C','D','S','CD','CS','DS','CDS']
                    }
                },
                {
                    "headerName": "Effekte",
                    "field": "effects",
                },
                {
                    "headerName": "Ton",
                    "field": "sound",
                },
                {
                    "headerName": "Tags",
                    "field": "tags",
                },
            ]
        }
    ]
}
searchgrid_options = {
    "defaultColDef": {
        "resizable": True,
        "sortable": True,
        "editable": True,
    },
    "columnDefs": [
        {
            "headerName": "ID",
            "field": "id",
            "mx-width": 200,

        },
        {
            "headerName": "Ergebnis",
            "field": "result",
            "wrapText": True,
            "autoHeight": True,
        },
    ]
}
st.set_page_config(page_title="Schöpferwissen",layout='wide')

basefolder = r"\\DATEN\Schoepferwissen"
datafolder = basefolder + r"\.DATA"

#if we don't find above path, ask for a new one
while not Path(datafolder).exists():
    with st.form('csv_form'):
        newfolder = st.text_input('CSV-Verzeichnis eingeben:', '')
        submitted = st.form_submit_button("OK")
        if not newfolder:
            st.stop()
        elif not Path(newfolder).exists():
            st.write('eingegebenen Pfad nicht gefunden')
            newfolder = None
            st.stop()
        else:
            datafolder = newfolder

loaded_csvs = glob.glob(os.path.join(datafolder, '*.csv'))
all_csvs = {}

# make a dict with all csvs
for i in range(len(loaded_csvs)):
    name = Path(loaded_csvs[i]).stem
    if "_aut" in name:
        name = name.replace("_automated", "")
        former_channel_name = name
    if "_man" in name:
        name = name.replace("_manuell", "")
        if former_channel_name == name:
            name = "merge" + name
    all_csvs[name] = loaded_csvs[i]

lastchosen = 'None'
lastftfilter = ''
if 'total_length' not in st.session_state: st.session_state.total_length = ''

col1, col2 = st.columns([2, 1])
with col1:
    chosen_csv = st.radio('', [[*all_csvs][i] for i in range(len(all_csvs)) if not "merge" in [*all_csvs][i]])
with col2:
    titlefilter = st.text_input('Titelsuche', '')
    descriptionfilter = st.text_input('Beschreibungssuche (YT)', '')
    tagfilter = st.text_input('Tagsuche (YT & manuell)', '')

#open chosen channel data and merge automated and manual csvs
with open(all_csvs[chosen_csv], 'r', encoding='utf-8') as csv:
    imported = pd.read_csv(csv, encoding='utf-8')
    current_index = [*all_csvs].index(chosen_csv)
    if "merge" in [*all_csvs][current_index+1]:
        with open(list(all_csvs.values())[current_index+1], 'r', encoding='utf-8') as csv2:
            imported2 = pd.read_csv(csv2, encoding='utf-8')
            imported = pd.merge(imported, imported2, on='id', sort=False, how="left", validate="one_to_one")

col3, col4 = st.columns([2, 1])
with col3:
    st.write('# ', chosen_csv)
    st.write(str(imported.shape[0]), " Videos (Gesamtspielzeit: ", convert_time(int(imported['length'].sum())), ")")
with col4:
    if not Path(basefolder).exists():
        st.warning("Videoarchiv nicht gefunden. Volltextsuche ist deaktiviert.")
        fulltextfilter = ''
    else:
        fulltextfilter = st.text_input('Volltextsuche', '')

#merge with list of archived videos
archived = pd.read_csv(PurePath(basefolder).joinpath(chosen_csv, 'download-archive.txt'), sep=" ", header=None)
archived.columns = ["platform", "id"]
archived['platform'] = '✓'
imported = pd.merge(imported, archived, on='id', how='outer')
#and clean up possible newly introduced nans
imported['platform'] = imported['platform'].replace(numpy.nan, "×")
imported['age_restricted'] = imported['age_restricted'].replace(numpy.nan, False)
imported['keywords'] = imported['keywords'].replace(numpy.nan, "[]")
number_cols = ['length', 'views']
imported[number_cols] = imported[number_cols].replace(numpy.nan, 0)
imported = imported.replace(numpy.nan, " ")

#filter/drop some stuff before displaying
caption_codes = {'a.de': 'auto de', 'a.en': 'auto en', 'a.fr': 'auto fr', 'a.it': 'auto it', 'a.vi': 'auto vi', 'a.es': 'auto es', 'a.nl': 'auto nl', 'a.ko': 'auto ko', 'a.ru': 'auto ru', 'a.id': 'auto id', '{}': ''}
try:
    imported = imported.drop(['yt_caption_tracks', 'vid_info'], axis=1)
    for c in caption_codes:
        imported.loc[imported['yt_caption_info'].str.contains(c, na= False), 'yt_caption_info'] = caption_codes[c]
    imported.loc[imported['description'].str.contains('<NA>', na= True), 'description'] = ''
    #imported['keywords'] = imported['keywords'].str.replace(r'\[\'\]', '')
except:
    pass

#convert seconds to min:sek format, clean up keywords
imported['length'] = imported['length'].apply(convert_time)
imported['keywords'] = imported['keywords'].apply(cleanup_tags)

#apply user filters
try:
    filt1 = imported['title'].str.contains(titlefilter, na=False, case=False)
    filt2 = imported['description'].str.contains(descriptionfilter, na=False, case=False)
    filt3 = imported['keywords'].str.contains(tagfilter, na=False, case=False)
    filt3 = pd.concat([filt3, imported['tags'].str.contains(tagfilter, na=False, case=False)], axis=1)
    imported_filt = imported.loc[filt1 & filt2 & filt3.any(axis=1)]
except:
    imported_filt = imported

#render main table
if 'interactive' not in st.session_state: st.session_state['interactive'] = {}
st.session_state.interactive = AgGrid(imported_filt, grid_options, fit_columns_on_grid_load=True, allow_unsafe_jscode=True, update_mode='VALUE_CHANGED', reload_data=False)

#write our current folder in the archive for control
st.write(PurePath(basefolder).joinpath(chosen_csv), archived.shape[0])

#render an additional table for fulltextsearch
if fulltextfilter != lastftfilter:
    search = ft_search.searchText(fulltextfilter, PurePath(basefolder).joinpath(chosen_csv))
    searchresults = pd.DataFrame(search.list_sentences)
    search_table = AgGrid(searchresults, searchgrid_options)
    lastftfilter = fulltextfilter

#watch a specific video from the archive by inputting its ID
video_id = st.text_input('Video anschauen (ID eingeben)', '')
use_archive = st.checkbox('aus dem Archiv laden')
if video_id != '':
    if video_id in imported_filt['id'].values:
        video_file_list = []
        if use_archive:
            video_folder = Path(basefolder).joinpath(chosen_csv)
            files_with_id = video_folder.glob(f'*{video_id}*')
            for f in files_with_id:
                if f.suffix in ['.mp4', '.mkv', '.webm']: video_file_list.append(f)
            if len(video_file_list) > 0:
                video_file = open(video_file_list[0], 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes, format="video/mp4")
            else:
                st.error("Videodatei nicht gefunden")
        else:
            st.video(f"https://youtu.be/{video_id}")
    else:
        st.error("ID nicht gefunden")

#prepare some variables for our clunky save mechanism
if 'reallysave' not in st.session_state: st.session_state['reallysave'] = False
if 'savefile' not in st.session_state: st.session_state['savefile'] = ''
if 'tosave' not in st.session_state: st.session_state['tosave'] = st.session_state.interactive["data"].drop(['publish_date', 'title', 'description', 'keywords', 'length', 'views', 'age_restricted', 'yt_caption_info', 'platform'], axis=1)
if 'oldsave' not in st.session_state: st.session_state['oldsave'] = {}
st.write(" ")

with st.form("saveform", clear_on_submit=True):
    if st.form_submit_button('Tabellenänderungen speichern'):
        st.session_state.tosave = st.session_state.interactive["data"].drop(['publish_date', 'title', 'description', 'keywords', 'length', 'views', 'age_restricted', 'yt_caption_info', 'platform'], axis=1)
        st.session_state.savefile = [s for s in loaded_csvs if chosen_csv+'_manuell' in s]
        st.session_state.oldsave = pd.read_csv(st.session_state.savefile[0], encoding='utf-8')
        st.write("### Änderungen:")
        #we turn IDs into index for comparing and later updating our dataframes
        st.session_state.oldsave = st.session_state.oldsave.set_index('id')
        st.session_state.tosave = st.session_state.tosave.set_index('id')
        df_diff = pd.concat([st.session_state.oldsave,st.session_state.tosave]).drop_duplicates(subset=['sentiments', 'effects', 'sound', 'behaviour', 'tags', 'people', 'location', 'CDS'], keep=False)
        df_diff
        st.session_state['reallysave'] = True

    if st.session_state['reallysave'] == True:
        reallybutton = st.empty()
        notreallybutton = st.empty()

        if reallybutton.form_submit_button('Wirklich speichern'):
            x = Path(st.session_state.savefile[0])
            bakcounter = 9

            #read the latest csv again, in case someone else has made changes in the meantime
            st.session_state.oldsave = pd.read_csv(st.session_state.savefile[0], encoding='utf-8')
            st.session_state.oldsave = st.session_state.oldsave.set_index('id')

            #merge updated cells into our old csv table and turn IDs back into a column
            st.session_state.oldsave.update(st.session_state.tosave)
            st.session_state.newsave = st.session_state.oldsave.rename_axis('id').reset_index()

            try:
                #we keep 10 backup files, with bak0 being the youngest
                while bakcounter > 0:
                    y = x.with_suffix(f'.bak{bakcounter}')
                    z = x.with_suffix(f'.bak{bakcounter-1}')
                    if Path(y).exists():
                        z.replace(y)
                    elif Path(z).exists():
                        z.replace(y)
                    bakcounter += -1
                x.replace(x.with_suffix(f'.bak{bakcounter}'))
                st.session_state.newsave.to_csv(Path(x), index=False)
                st.success("CSV gespeichert")
                st.session_state['reallysave'] = False
            except:
                st.error("Irgendwas ging schief (sorry)")
                st.session_state['reallysave'] = False
        elif notreallybutton.form_submit_button('Abbrechen'):
            reallybutton.empty()
            notreallybutton.empty()
            st.session_state['reallysave'] = False

#    with st.expander("Vorher/Nachher anzeigen"):
#        st.write(st.session_state.tosave.compare(st.session_state.oldsave, align_axis=0, keep_equal=True).rename(index={'self': 'neu', 'other': 'alt'}, level=-1))
