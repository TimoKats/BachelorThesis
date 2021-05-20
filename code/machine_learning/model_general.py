# speed and power...solves many many things. -Jeremy Clarkson
# name:         model_general.py
# author:       Timo Kats
# last update:  20/05/2021
# description:  Does the general machine learning tasks. See tables 2-3, 11-12 in thesis.

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
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

def export_model(source, representation, learning_model, accuracy, f1_score, roc_auc):
    f = open('results/csv/results.csv', 'a+', encoding='utf-8')
    string = str(source + ',' + representation + ',' +  learning_model + ',' + accuracy +  ',' + f1_score + ',' + roc_auc + '\n')
    print(string)
    f.write(string)
    f.close()

def export_features(representation, features, accuracy, f1_score, roc_auc):
    #f = open('results/csv/results_features.csv', 'a+', encoding='utf-8')
    string = str(representation  +  ',' + str(features)  + ',' + accuracy + ',' + f1_score + ',' + roc_auc + '\n')
    print(string)
    #f.write(string)
    #f.close()

def export_svm(features, kernel, decision_function_shape, accuracy, f1_score, roc_auc):
    print(features, kernel, decision_function_shape, accuracy, f1_score, roc_auc, sep=',')
    return

def get_target(dataframe):
    dataframe['is_sponsored'] = np.where(dataframe['sponsor'] != 'none', 1, 0)
    return dataframe['is_sponsored']

def get_data(source):
    data_ads = pd.read_csv('data/ads/ads_' + source + '.csv')
    data_articles = pd.read_csv('data/articles/articles_' + source + '.csv')
    data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)
    data['input'] = data['introduction'] + ' ' + data['body']
    return data

def get_x(data, transformer, feature):
    data = data['input'].values.astype('U')
    file = open('data/stopwords', 'r+', encoding='utf-8')
    stop_words = file.read().split('\n')

    if transformer == 'bag of words':
        cv = CountVectorizer(stop_words = stop_words, lowercase=True, max_features=feature)
    elif transformer == 'tfidf':
        cv = TfidfVectorizer(stop_words = stop_words, lowercase=True, max_features=feature)
    cv.fit(data)
    X = cv.transform(data)
    return X

def run_model(X, y, source, representation, learning_model, feature):

    if learning_model == 'svm':
        clf = svm.SVC(max_iter=5000, cache_size=2000)
    elif learning_model == 'decisionTree':
        clf = DecisionTreeClassifier(random_state=0, max_depth=None)
    elif learning_model == 'SGD':
        clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5000)
    elif learning_model == 'k-NN':
        clf = KNeighborsClassifier()
    elif learning_model == 'randomForest':
        clf = RandomForestClassifier(max_depth=None)
    elif learning_model == 'naiveBayes':
        X = X.toarray()
        clf = GaussianNB()
    else:
        clf = LinearSVC(max_iter=5000)

    scores = cross_val_score(clf, X, y, cv=10, scoring='accuracy')
    accuracy = str(round(scores.mean(), 4)) + '±' + str(round(scores.std(), 4))

    scores = cross_val_score(clf, X, y, cv=10, scoring='roc_auc')
    roc_auc = str(round(scores.mean(), 4)) + '±' + str(round(scores.std(), 4))

    scores = cross_val_score(clf, X, y, cv=10, scoring='f1')
    f1_score = str(round(scores.mean(), 4)) + '±' + str(round(scores.std(), 4))

    export_features(representation, feature, accuracy, f1_score, roc_auc)
    #export_model(source, representation, learning_model, accuracy, f1_score, roc_auc)

def run_svm(X, y, source, representation, features, kernel, decision_function_shape):
    clf = svm.SVC(max_iter=5000, cache_size=2000, kernel=kernel, decision_function_shape=decision_function_shape, random_state=12)
    scores = cross_val_score(clf, X, y, cv=10, scoring='accuracy')
    accuracy = str(round(scores.mean(), 4)) + '±' + str(round(scores.std(), 4))

    scores = cross_val_score(clf, X, y, cv=10, scoring='roc_auc')
    roc_auc = str(round(scores.mean(), 4)) + '±' + str(round(scores.std(), 4))

    scores = cross_val_score(clf, X, y, cv=10, scoring='f1')
    f1_score = str(round(scores.mean(), 4)) + '±' + str(round(scores.std(), 4))

    export_svm(features, kernel, decision_function_shape, accuracy, f1_score, roc_auc)

if __name__ == '__main__':

    sources = ['nu', 'telegraaf', 'nrc', 'ondernemer', 'totaal']
    input_models = ['tfidf']
    learning_models = ['svm']
    kernels = ['linear']
    decision_function_shapes = ['ovo']
    #features = [1, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, None]
    features = 5000

    #export_model('source', 'representation', 'learning model', 'accuracy', 'f1 score', 'roc_auc')


    for source in sources:
        data = get_data(source)
        for input_model in input_models:
            y = get_target(data)
            X = get_x(data, input_model, 5000)
            for learning_model in learning_models:
                run_model(X, y, source, input_model, learning_model, 5000)

    '''
    export_features('representation', 'features', 'accuracy', 'f1 score', 'roc_auc')

    for source in sources:
        data = get_data(source)
        for input_model in input_models:
            for feature in features:
                y = get_target(data)
                X = get_x(data, input_model, feature)
                for learning_model in learning_models:
                        run_model(X, y, source, input_model, learning_model, feature)
 

    for source in sources:
        data = get_data(source)
        y = get_target(data)
        X = get_x(data, 'tfidf', features)
        for kernel in kernels:
            for decision_function_shape in decision_function_shapes:
                run_svm(X, y, source, 'tfidf', features, kernel, decision_function_shape)

    '''