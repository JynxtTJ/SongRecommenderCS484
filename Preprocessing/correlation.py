import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('../data/data.csv')

print(data.loc[0])

data = data.iloc[:, 1:]
data = data.drop('danceability', 1)

print(data['energy'].value_counts())

corr = data.corr()

print(corr)

sns.set(rc = {'figure.figsize':(15,15)})
sns.heatmap(corr, annot=True)
plt.show()
