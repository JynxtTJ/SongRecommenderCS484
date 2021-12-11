import pandas as pd

from sklearn.preprocessing import LabelEncoder


def enest_terms_label_encoding(data_path):
    data = pd.read_csv(data_path, index_col=0)

    if data is not None:
        categories = data['enest terms']
        # Creating a label encoder to reformat enest terms
        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(categories)

        data['enest terms'] = integer_encoded

        data.to_csv(data_path)


if __name__ == "__main__":
    enest_terms_label_encoding('../data/data.csv')
