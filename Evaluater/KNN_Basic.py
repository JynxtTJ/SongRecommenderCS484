
# num_found = 0
#
# for datum in data.itertuples():
#     search_term = datum[10]
#     result = data['title'].str.contains(search_term, case=False)
#
#     if result.empty:
#         print("Not found " + str(search_term))
#     else:
#         num_found += 1
#
# print(num_found)

# song = "I Didn't Mean To"
# artist = "Casual"
#
# song_and_artist_data = data[(data['title'] == song) & (data['artist name'] == artist)]
#
# similar = data.copy()
#
# sound_properties = similar.loc[:, ['key', 'key confidence', 'duration', 'hotness', 'energy', 'loudness', 'tempo']]
#
# similar['Similarity'] = cosine_similarity(sound_properties, sound_properties.to_numpy()[song_and_artist_data.index[0], None]).squeeze()
#
# print(similar)


def get_similar_songs(dataset, song, artist):
    song_and_artist_data = dataset[(dataset['title'] == song) & (dataset['artist name'] == artist)]

    similar = dataset.copy()

    sound_properties = similar.loc[:, ['key', 'key confidence', 'duration', 'hotness', 'energy', 'loudness', 'tempo', 'mode', 'mode_confidence', 'danceability']]

    similar['Similarity'] = cosine_similarity(sound_properties, sound_properties.to_numpy()[
        song_and_artist_data.index[0], None]).squeeze()

    similar = similar.sort_values(by='Similarity', ascending=False)

    similar_songs = similar[[f'title', 'artist name', 'album', 'year', 'Similarity']]

    return similar_songs.iloc[2:12]


pd.set_option("display.max_rows", None, "display.max_columns", None)
print(get_similar_songs(data, "Panama (Remastered Album Version)", "Van Halen"))
