# speed and power...solves many many things. -Jeremy Clarkson
# name:         model_cross_source.py
# author:       Timo Kats
# last update:  20/05/2021
# description:  Does cross validation through news sources. See tables 4-10 in thesis.

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from collections import OrderedDict
from keras.preprocessing.text import Tokenizer

import sklearn
from sklearn import svm, preprocessing
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import confusion_matrix, roc_auc_score, f1_score
from sklearn.model_selection import cross_val_score

def get_y(data):
    data['is_sponsored'] = np.where(data['sponsor'] != 'none', 1, 0)
    return data['is_sponsored']

def get_X(data_total, data):

    file = open('data/stopwords', 'r+', encoding='utf-8')
    stop_words = file.read().split('\n')

    data = data['input'].values.astype('U')
    data_total = data_total['input'].values.astype('U')

    vectorizer = TfidfVectorizer(stop_words = stop_words)
    vectorizer.fit_transform(data_total)
    data_total = vectorizer.get_feature_names()

    cv = TfidfVectorizer(vocabulary=data_total, stop_words = stop_words, lowercase=True, max_features=None)
    cv.fit(data)
    X = cv.transform(data)
    return X

def get_data_train(source):
    data_ads = pd.read_csv('data/ads/ads_totaal.csv')
    data_articles = pd.read_csv('data/articles/articles_totaal.csv')
    data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)

    indexNames = data[data['source'] != source].index
    data.drop(indexNames, inplace=True)
    data = data.reset_index(drop=True)
    data['input'] = data['introduction'] + ' ' + data['body']
    return data[['sponsor', 'input']]

def get_data_test(source):
    data_ads = pd.read_csv('data/ads/ads_totaal.csv')
    data_articles = pd.read_csv('data/articles/articles_totaal.csv')
    data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)

    indexNames = data[data['source'] != source].index
    data.drop(indexNames, inplace=True)
    data = data.reset_index(drop=True)
    data['input'] = data['introduction'] + ' ' + data['body']
    return data[['sponsor', 'input']]

def get_data_total():
    data_ads = pd.read_csv('data/ads/ads_totaal.csv')
    data_articles = pd.read_csv('data/articles/articles_totaal.csv')
    data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)
    data['input'] = data['introduction'] + ' ' + data['body']
    return data

def run_model(source, learning_model, X_test, y_test, X_train, y_train):

    if learning_model == 'svm':
        clf = svm.SVC(max_iter=5000)
    elif learning_model == 'decisionTree':
        clf = DecisionTreeClassifier(random_state=0, max_depth=None)
    elif learning_model == 'SGD':
        clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5000)
    elif learning_model == 'k-NN':
        clf = KNeighborsClassifier()
    elif learning_model == 'randomForest':
        clf = RandomForestClassifier(max_depth=None)
    elif learning_model == 'naiveBayes':
        X_train = X_train.toarray()
        X_test = X_test.toarray()
        clf = GaussianNB()
    else:
        clf = LinearSVC(max_iter=5000)

    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    print(learning_model, source, score, sep=',')

if __name__ == '__main__':

    sources = ['nrc', 'ondernemer', 'telegraaf', 'nu.nl']
    input_models = ['tfidf']
    learning_models = ['svm', 'linearSVC', 'decisionTree', 'randomForest', 'k-NN', 'SGD', 'naiveBayes']

    for source in sources:

        data_total = get_data_total()

        data_test = get_data_test(source)
        X_test = get_X(data_total, data_test)
        y_test = get_y(data_test)

        data_train = get_data_train(source)
        X_train = get_X(data_total, data_train)
        y_train = get_y(data_train)

        for learning_model in learning_models:
            run_model(source, learning_model, X_test, y_test, X_train, y_train)