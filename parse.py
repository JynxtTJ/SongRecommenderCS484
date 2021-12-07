import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np
import hdf5_getters as GETTERS

msd_subset = 'millionsongsubset'
# msd_subset_data_path = os.path.join(msd_subset, 'data')
# msd_subset_addf_path = os.path.join(msd_subset, 'AdditionalFiles')
# assert os.path.isdir(msd_subset)


def count_all_files(basedir,ext='.h5') :
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root,'*'+ext))
        cnt += len(files)
    return cnt

# def read_file_into_array(file):
#     h5 = h5fd_getters.open_h5_file_read(file)


print(count_all_files(msd_subset))
