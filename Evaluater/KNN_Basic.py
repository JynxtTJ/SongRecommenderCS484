import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances


def get_similar_songs(dataset, song, artist):
    song_and_artist_data = dataset[(dataset['title'] == song) & (dataset['artist name'] == artist)]

    distance = dataset.copy()

    sound_properties = distance.loc[:, ['key', 'key confidence', 'duration', 'hotness', 'energy', 'loudness',
                                       'tempo', 'mode', 'mode_confidence', 'danceability', 'enest terms']]

    distance['Similarity'] = euclidean_distances(sound_properties, sound_properties.to_numpy()[
        song_and_artist_data.index[0], None]).squeeze()

    distance = distance.sort_values(by='Similarity', ascending=True)

    similar_songs = distance[[f'title', 'artist name', 'album', 'year', 'Similarity']]

    return similar_songs.iloc[2:12]


def display_similar(path_to_data):
    data = pd.read_csv(path_to_data, index_col=0)

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(get_similar_songs(data, "Panama (Remastered Album Version)", "Van Halen"))


if __name__ == "__main__":
    data = pd.read_csv('../data/data.csv', index_col=0)

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(get_similar_songs(data, "Panama (Remastered Album Version)", "Van Halen"))
