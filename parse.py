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
from scipy.fft import fft

all_artist_names = set()
tags_set = []
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


def apply_to_all_files(basedir, func=lambda x: x, ext='.h5', doBreak=False, NTimes=0):
    cnt = 0
    count_val = -1

    if NTimes != 0:
        count_val = 0

    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*' + ext))
        cnt += len(files)
        for f in files:
            func(f)
            if doBreak:
                return cnt
            if NTimes != 0:
                count_val += 1
            if count_val == NTimes:
                return cnt

    return cnt


def func_to_get_artist_name(filename):
    h5 = GETTERS.open_h5_file_read(filename)

    artist_name = GETTERS.get_artist_name(h5)
    all_artist_names.add(artist_name)
    h5.close()


def func_get_tags(filename):
    h5 = GETTERS.open_h5_file_read(filename)

    mbtags = GETTERS.get_artist_mbtags(h5)
    print(mbtags)

    h5.close()

def func_get_enest_terms(filename):
    h5 = GETTERS.open_h5_file_read(filename)
    tags = GETTERS.get_artist_terms(h5)
    tags = tags.astype('str')

    tags_set.append(tags)

    h5.close()


def func_to_get_cfft(filename):
    h5 = GETTERS.open_h5_file_read(filename)

    chroma = GETTERS.get_segments_pitches(h5)
    chroma = np.array(chroma)
    chroma = chroma.transpose()
    print(chroma)
    sample_rate = GETTERS.get_analysis_sample_rate(h5)
    N, H = 2048, 1024

    Y = np.abs(chroma)
    plt.figure(figsize=(8, 3))
    plt.xlabel('Time (frames)')
    plt.ylabel('Frequency (bins)')

    plt.imshow(Y, aspect='auto', origin='lower')

    # librosa.display.specshow(librosa.amplitude_to_db(Y, ref=np.max),
    #                          y_axis='linear', x_axis='time', sr=sample_rate, hop_length=H)

    plt.tight_layout()
    plt.colorbar()
    plt.show()
    print('The spectrogram Y has %d frequency bins and %d frames.' % (Y.shape[0], Y.shape[1]))
    h5.close()


def get_data(filename):
    h5 = GETTERS.open_h5_file_read(filename)

    song_datum = []

    # ----------------- DATA POINTS -----------------

    song_datum.append(GETTERS.get_key(h5))  # shape = 1 [1, 12]
    song_datum.append(GETTERS.get_key_confidence(h5))  # shape = 1
    # These are interested as we can weight our key_score based on the key_conf by simple multiplication.

    song_datum.append(GETTERS.get_duration(h5))
    song_datum.append(GETTERS.get_artist_hotttnesss(h5))  # shape = 1 (on range [0,1])
    song_datum.append(GETTERS.get_energy(h5))  # shape = 1 (on range [0, 1])
    song_datum.append(GETTERS.get_loudness(h5))  # shape = 1 (db range)

    # WE want similar songs, not artists, while artists is useful we cannot simply base our
    # recommendation off an artist that is similar.
    # similar_artists = GETTERS.get_similar_artists(h5)  # shape = (935,0) (datum is string)

    song_datum.append(GETTERS.get_tempo(h5))  # shape = 1 (datum is BPM)

    song_datum.append(GETTERS.get_mode(h5))
    song_datum.append(GETTERS.get_mode_confidence(h5))

    song_datum.append(GETTERS.get_danceability(h5))

    # ----------------- TRACK INFO -----------------

    song_datum.append(GETTERS.get_year(h5))

    release = GETTERS.get_release(h5)
    release = release.decode('utf-8')
    song_datum.append(release)

    artist_name = GETTERS.get_artist_name(h5)
    artist_name = artist_name.decode('utf-8')
    song_datum.append(artist_name)  # shape = 1 (datum is string)

    title = GETTERS.get_title(h5)
    title = title.decode('utf-8')
    song_datum.append(title)

    tags = GETTERS.get_artist_terms(h5)
    tags = tags.astype('str')

    song_datum.append(tags)

    # chroma_fft = GETTERS.get_segments_pitches(h5)
    # chroma_fft = fft(chroma_fft).real
    # song_datum.append(chroma_fft)

    data_set.append(song_datum)
    h5.close()

# Chroma Analysis
# apply_to_all_files(msd_subset, func=func_to_get_cfft, doBreak=True)

# Tag Analysis
# This one is too inconsistent to be useful
# apply_to_all_files(msd_subset, func=func_get_tags)


# apply_to_all_files(msd_subset, func=func_get_enest_terms, NTimes=2)
# for x in tags_set:
#     print(x)


apply_to_all_files(msd_subset, func=get_data)
main_dataframe = pd.DataFrame(data_set,
                              columns=['key', 'key confidence', 'duration', 'hotness', 'energy', 'loudness', 'tempo',
                                       'mode', 'mode_confidence', 'danceability', 'year', 'album', 'artist name',
                                       'title', 'enest terms'])
main_dataframe.to_csv('data/data.csv')

