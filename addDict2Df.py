from pandas import DataFrame
from matplotlib.pyplot import get
from youtube_transcript_api import YouTubeTranscriptApi

data = {
    'title': [],
    'Youtube ID': [],
    'views': [],
    'description': [],
    'date_published': [],
    'duration': [],
    'tags': [],
    'transcript': [],
    'transcript language': [],
    'transcript auto-generated': [],
    'transcript translatable': [],
}

df = DataFrame(data)

def addDict2Df(metadata_dict, id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(id)
    transcript = transcript_list.find_transcript(['de', 'en'])

    title = metadata_dict.get("title")
    views = metadata_dict.get("views")
    description = metadata_dict.get("description")
    date_published = metadata_dict.get("date_published")
    duration = metadata_dict.get("duration")
    tags = metadata_dict.get("tags")
    transcript_fetch = transcript.fetch()
    transcript_language = transcript.language_code
    transcript_auto_generated = transcript.is_generated
    transcript_translatable = transcript.is_translatable

    df.loc[df.shape[0]] = [title, id,  views, description, date_published, duration, tags, transcript_fetch, transcript_language, transcript_auto_generated, transcript_translatable]
    print(df)
    return df
