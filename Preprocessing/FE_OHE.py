import pandas as pd
import numpy as np
import traceback
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('../data/data.csv', index_col=0)
#print(data.head())


def get_similar_songs(dataset, song, artist):
    #song = "We Will Rock You"
    #artist = "Nickelback"

    song_and_artist_data = dataset[(dataset['title'] == song) & (dataset['artist name'] == artist)]
    #print(song_and_artist_data)

    similar = dataset.copy()

    sound_properties = similar.loc[:, ['key', 'key confidence', 'duration', 'hotness', 'energy', 'loudness', 'tempo']]

    similar['Similarity'] = cosine_similarity(sound_properties, sound_properties.to_numpy()[
        song_and_artist_data.index[0], None]).squeeze()

    similar = similar.sort_values(by='Similarity', ascending=False)
    #print(similar)

    similar_songs = similar[[f'title', 'artist name', 'album', 'year', 'Similarity']]
    #print(similar_songs)

    return similar_songs.iloc[2:12]


pd.set_option("display.max_rows", None, "display.max_columns", None)
print(get_similar_songs(data, "Panama (Remastered Album Version)", "Van Halen"))
