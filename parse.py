import os
import sys
import time
import glob
import datetime
import numpy as np
import pandas as pd

import hdf5_getters as GETTERS
import matplotlib.pyplot as plt
import librosa
import librosa.display
import csv
import pandas as pd

all_artist_names = set()
data_set = []

msd_subset = 'millionsongsubset'


# msd_subset_data_path = os.path.join(msd_subset, 'data')
# msd_subset_addf_path = os.path.join(msd_subset, 'AdditionalFiles')
# assert os.path.isdir(msd_subset)


def count_all_files(basedir, ext='.h5'):
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*' + ext))
        cnt += len(files)

    return cnt


def apply_to_all_files(basedir, func=lambda x: x, ext='.h5'):
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*' + ext))
        cnt += len(files)
        for f in files:
            func(f)

    return cnt


def func_to_get_artist_name(filename):
    h5 = GETTERS.open_h5_file_read(filename)

    artist_name = GETTERS.get_artist_name(h5)
    all_artist_names.add(artist_name)
    h5.close()


def get_data(filename):

    h5 = GETTERS.open_h5_file_read(filename)

    song_datum = []

    song_datum.append(GETTERS.get_key(h5)) # shape = 1 [1, 12]
    song_datum.append(GETTERS.get_key_confidence(h5)) # shape = 1
    # These are interested as we can weight our key_score based on the key_conf by simple multiplication.

    song_datum.append(GETTERS.get_duration(h5))
    song_datum.append(GETTERS.get_artist_hotttnesss(h5)) # shape = 1 (on range [0,1])
    song_datum.append(GETTERS.get_energy(h5))  # shape = 1 (on range [0, 1])
    song_datum.append(GETTERS.get_loudness(h5)) # shape = 1 (db range)

    # WE want similar songs, not artists, while artists is useful we cannot simply base our
    # recommendation off an artist that is similar.
    # similar_artists = GETTERS.get_similar_artists(h5)  # shape = (935,0) (datum is string)

    song_datum.append(GETTERS.get_tempo(h5)) # shape = 1 (datum is BPM)

    # HIHGLY INTERESTING FEATURE.
    # chroma_pitches.append(GETTERS.get_segments_pitches(h5))  # = shape (935, 12) normallized so range [0, 1]

    song_datum.append(GETTERS.get_artist_name(h5)) # shape = 1 (datum is string)
    song_datum.append(GETTERS.get_title(h5))

    data_set.append(song_datum)
    h5.close()


apply_to_all_files(msd_subset, func=get_data)

main_dataframe = pd.DataFrame(data_set, columns=['key', 'key confidence', 'duration', 'hotness', 'energy', 'loudness', 'tempo', 'artist name', 'title'])

main_dataframe.to_csv('data/data.csv')
