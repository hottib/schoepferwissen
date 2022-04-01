from pandas import DataFrame

data = {
    'title': [],
    'views': [],
    'description': [],
    'date_published': [],
    'duration': [],
    'tags': [],
}

df = DataFrame(data)

def addDict2Df(metadata_dict):
    title = metadata_dict.get("title")
    views = metadata_dict.get("views")
    description = metadata_dict.get("description")
    date_published = metadata_dict.get("date_published")
    duration = metadata_dict.get("duration")
    tags = metadata_dict.get("tags")
    df.loc[df.shape[0]] = [title, views, description, date_published, duration, tags]
    print(df)
    return df