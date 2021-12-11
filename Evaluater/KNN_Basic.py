import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances


data = pd.read_csv('../data/data.csv', index_col=0)


def get_similar_songs(dataset, song, artist):
    song_and_artist_data = dataset[(dataset['title'] == song) & (dataset['artist name'] == artist)]

    similar = dataset.copy()

    sound_properties = similar.loc[:, ['key', 'key confidence', 'duration', 'hotness', 'energy', 'loudness', 'tempo', 'mode', 'mode_confidence', 'danceability', 'enest terms']]

    similar['Similarity'] = euclidean_distances(sound_properties, sound_properties.to_numpy()[
        song_and_artist_data.index[0], None]).squeeze()

    similar = similar.sort_values(by='Similarity', ascending=True)

    similar_songs = similar[[f'title', 'artist name', 'album', 'year', 'Similarity']]

    return similar_songs.iloc[2:12]


pd.set_option("display.max_rows", None, "display.max_columns", None)
print(get_similar_songs(data, "Panama (Remastered Album Version)", "Van Halen"))
