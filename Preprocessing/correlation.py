import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def main():
    data = pd.read_csv('../data/data.csv')

    data = data.iloc[:, 1:]
    data = data.drop('danceability', 1)

    print(data['energy'].value_counts())

    corr = data.corr()

    sns.set(rc={'figure.figsize': (15, 15)})
    sns.clustermap(corr, annot=True, cmap="vlag")
    plt.show()


if __name__ == "__main__":
    main()
