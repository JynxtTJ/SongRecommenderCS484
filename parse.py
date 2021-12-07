import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np
import hdf5_getters as GETTERS

all_artist_names = set()

msd_subset = 'millionsongsubset'
# msd_subset_data_path = os.path.join(msd_subset, 'data')
# msd_subset_addf_path = os.path.join(msd_subset, 'AdditionalFiles')
# assert os.path.isdir(msd_subset)


def count_all_files(basedir, ext='.h5'):
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        cnt += len(files)
    return cnt


def apply_to_all_files(basedir, func=lambda x: x, ext='.h5'):
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*'+ext))
        cnt += len(files)
        for f in files:
            func(f)

    return cnt


def func_to_get_artist_name(filename):
    h5 = GETTERS.open_h5_file_read(filename)

    artist_name = GETTERS.get_artist_name(h5)
    all_artist_names.add(artist_name)
    h5.close()


print(count_all_files(msd_subset))

apply_to_all_files(msd_subset, func=func_to_get_artist_name)

for k in range(5):
    print(list(all_artist_names)[k])
