# speed and power...solves many many things. -Jeremy Clarkson
# name:         make_tsne.py
# author:       Timo Kats
# last update:  20/05/2021
# description:  makes tsne graphs per news source.

import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gensim

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import svm, preprocessing
from sklearn.manifold import TSNE
from sklearn.model_selection import cross_val_score, train_test_split

def get_stopwords():
    file = open('data/stopwords', 'r+', encoding='utf-8')
    stop_words = file.read().split('\n')
    return stop_words

def get_data(dataframe):
    dataframe['is_sponsored'] = np.where(dataframe['sponsor'] != 'none', 1, 0)
    return dataframe['is_sponsored']

def get_classes(dataframe):
    dataframe['class'] = np.where(dataframe['sponsor'] != 'none', 'advertorial', 'article')
    return dataframe['class']

if __name__ == '__main__':

    sources = ['nu', 'telegraaf', 'nrc', 'ondernemer']

    for source in sources:
        data_ads = pd.read_csv('data/ads/ads_' + source + '.csv')
        data_articles = pd.read_csv('data/articles/articles_' + source + '.csv')
        data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)
        data['input'] = data['introduction'] + ' ' + data['body']
        is_sponsored = get_classes(data).tolist()
        source = data['source'].tolist()
        y = get_data(data)

        data = data['input'].values.astype(str)

        stop_words = get_stopwords()
        cv = TfidfVectorizer(stop_words=stop_words, lowercase=True, max_features=5000)
        cv.fit(data)

        X = cv.transform(data)

        clf = svm.SVC(max_iter=5000, cache_size=50000)
        clf.fit(X, y)
        clf.predict(X)

        model = TSNE(random_state=2)
        tsne_features = model.fit_transform(X)

        df = pd.DataFrame()
        df['x'] = tsne_features[:,0]
        df['y'] = tsne_features[:,1]
        df['class'] = is_sponsored
        df['source'] = source
        print(df)

        sns.scatterplot(x='x', y='y', hue='class', data=df, palette=['blue', 'red'])
        plt.show()
