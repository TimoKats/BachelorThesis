import pandas as pd
import random

def get_data():
    pd.options.display.max_colwidth = 500
    data_ads = pd.read_csv('data/advertorials.csv')
    data_art = pd.read_csv('data/articles.csv')
    data_ads = data_ads[['title']]
    data_art = data_art[['title']]
    frames = [data_ads, data_art]
    return pd.concat(frames, ignore_index=True)

def question(data):
    correct_answer = random.randint(0,2000)
    question = data.iloc[correct_answer]['title']
    user_answer = ""
    print('is -', question, '- and article or an advertorial?')
    user_answer = input('type 1 for article or 2 for advertorial!\n>>> ')
    if (user_answer is '1' and correct_answer > 1000) or (user_answer is '0' and correct_answer <= 1000):
        print('correct!')
    else:
        print('false!')

if __name__ == '__main__':
    data = get_data()
    operator = ""

    print('Welcome to "Differentiating Advertorials and Articles" the video game.')
    while True:
        operator = input('\npress 1 for a question, press 2 to quit\n>>> ')
        if operator is '2':
            break
        elif operator is '1':
            question(data)
        else:
            print('input not recognized')

    print('Thanks for playing "Differentiating Advertorials and Articles" the video game.')
