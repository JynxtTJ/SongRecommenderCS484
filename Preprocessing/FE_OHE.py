import pandas as pd
import numpy as np
import sklearn

from sklearn.metrics.pairwise import cosine_similarity
import traceback

data = pd.read_csv('../data/data.csv', index_col=0)