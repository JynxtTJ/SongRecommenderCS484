import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


data = pd.read_csv('../data/data.csv', index_col=0)

if data is not None:
    categories = data['enest terms']
    # Creating a label encoder to reformat enest terms
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(categories)

    print(integer_encoded)
    print(len(integer_encoded))

    data['enest terms'] = integer_encoded

    data.to_csv('../data/data.csv')

