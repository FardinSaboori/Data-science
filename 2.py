import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# importing Data
movies = pd.read_csv('C:/Users/15877/PycharmProjects/Calculator/movies.csv', sep=',')
tags = pd.read_csv('C:/Users/15877/PycharmProjects/Calculator/tags.csv', sep=',')
ratings = pd.read_csv('C:/Users/15877/PycharmProjects/Calculator/ratings.csv', sep=',', parse_dates=['timestamp'])

row_zero = tags.iloc[[0, 11, 100]]
# df.drop(df.index[[5]]) 'row removal'
filterr = ratings['rating'] > 4.5
# print(movies[:6])
tags = tags.dropna()
# print(tags.isnull().any())
filter2 = ratings['rating'] >= 4
# print(ratings[filter2][-5:])
filter3 = movies['genres'].str.contains('Animation')
# print(movies[filter3])

# splitting and extracting data from each cell
moviesgenres = movies['genres'].str.split('|', expand =True)
# print(moviesgenres[:5])
moviesgenres['comedy_column'] = movies['genres'].str.contains('Comedy')
# print(moviesgenres[:5])
movies['year'] = movies['title'].str.extract('.*\((.*)\).*', expand=True)
# print(moviesgenres[:5])

# Parsing time
tags['parsed_time'] = pd.to_datetime(tags['timestamp'], unit='s')
# print(tags.sort_values(by='parsed_time', ascending=True))

# aggregating and groupby:
avg = ratings[["rating", "movieId"]].groupby('movieId', as_index=False).mean()
boxoffice = movies.merge(avg, on='movieId', how='inner')
# print(boxoffice[:5])
yearly_average = boxoffice[['year','rating']].groupby('year', as_index=False).mean()
print(yearly_average[:10])
yearly_average[-20:].plot('year', 'rating', figsize=(15,10))
# plt.show()
# we can conclude that there are some outliers tha can be eliminated from our dataset for future predictions.
# so we git rid of the outliers:
lowerbound = 0.05
upperbound = 0.96
res = yearly_average['rating'].quantile([lowerbound, upperbound])
print(res)
true = (res.loc[lowerbound] < yearly_average['rating'].values) & (yearly_average['rating'].values < res.loc[upperbound])
false = ~ true
x = yearly_average['rating']
avg = np.mean(x[true])
print(avg)
x.replace(x[false], avg, inplace=True)
print(x)

# creating filters
highly_rated = boxoffice['rating'] >= 4.0
comedy = boxoffice['genres'].str.contains('Comedy')
# print(boxoffice[comedy & highly_rated][-5:])

