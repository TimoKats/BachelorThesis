# speed and power...solves many many things. -Jeremy Clarkson
# name:         model_lexicon.py
# author:       Timo Kats
# last update:  20/05/2021
# description:  Does the lexicon formula described in the thesis. aka the timo algorithm :)

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def get_input(source):
    data_ads = pd.read_csv('data/ads/ads_' + source + '.csv')
    data_articles = pd.read_csv('data/articles/articles_' + source + '.csv')
    data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)
    data['input'] = data['introduction'] + ' ' + data['body']
    data['input'] = data['input'].values.astype(str)
    return data

def get_target(source):
    data_ads = pd.read_csv('data/ads/ads_' + source + '.csv')
    data_articles = pd.read_csv('data/articles/articles_' + source + '.csv')
    data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)
    data['is_sponsored'] = np.where(data['sponsor'] != 'none', 1, 0)
    return data['is_sponsored']

def get_sources(source):
    data_ads = pd.read_csv('data/ads/ads_' + source + '.csv')
    data_articles = pd.read_csv('data/articles/articles_' + source + '.csv')
    data = pd.DataFrame(data_ads).append(data_articles, ignore_index=True)
    return data['source']

def get_top_features():
    data = pd.read_csv('data/lexicon2.csv')
    return data['word']

def get_top_scores():
    data = pd.read_csv('data/lexicon2.csv')
    return data['score']

def make_vector(entries, features, representation):
    if representation == 'tfidf':
        vectorizer = TfidfVectorizer(vocabulary=features, lowercase=True)
    else:
        vectorizer = CountVectorizer(vocabulary=features, lowercase=True)
    X = vectorizer.fit_transform(entries)
    return pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())

def timo_algorithm(data, features, scores):
    result, result_total = [], []
    for index, row in data.iterrows():
        result = []
        frequencies = row.tolist()
        for score, frequency in zip(scores, frequencies):
            result.append(score * frequency)
        result_total.append(sum(result))
    return result_total

def get_score(results, answers, sources):
    correct_answers= 0
    f = open('../graphs/lexicon_scores.csv', 'a', encoding='utf-8')
    f.write('score,result,answer,source\n')

    for (res, ans, src) in zip(results, answers, sources):
        if res > 0:
            classified_result = 1
        else:
            classified_result = 0

        if classified_result == ans:
            correct_answers += 1

        print(res, classified_result, ans, src)
        f.write(str(res) + ',' + str(classified_result) + ',' + str(ans) + ',' + str(src) + '\n')

    return (correct_answers/len(answers))

if __name__ == '__main__':
    data = get_input('totaal')
    entries = data['input']
    features = get_top_features().tolist()
    sources = get_sources('totaal').tolist()
    scores = get_top_scores()
    answers = get_target('totaal').tolist()


    data = make_vector(entries, features, 'tfidf')

    # het timo algoritme...
    results = timo_algorithm(data, features, scores)
    accuracy = get_score(results, answers, sources)

    print('final score with tfidf:            ', accuracy)

    '''
    data = make_vector(entries, features, 'bow')

    # het timo algoritme...
    results = timo_algorithm(data, features, scores)
    accuracy = get_score(results, answers)

    print('final score with bag of words:     ', accuracy)
    '''