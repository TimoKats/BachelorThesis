# speed and power...solves many many things. -Jeremy Clarkson
# name:         url_scraper_telegraaf.py
# author:       Timo Kats
# last update:  20/05/2021
# description:  Brute force scraping algorithm for telegraaf. See algorithm 2 in thesis.

from bs4 import BeautifulSoup
import requests
import re

def get_articles(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.find_all("a", class_="ArchivePage__link")
    text = str(text)
    index_2 = 0
    count = 0
    ads = []
    while count < 10:
        index_1 = text.find('href="', index_2)
        index_2 = text.find('">', index_1 + 1)
        ads.append(text[index_1+6:index_2])
        count += 1
    return ads

def export_articles(list):
    file = open('articles.txt', 'a+')
    for article in list:
        file.write(article + '\n')

if __name__ == '__main__':

    dag = 1
    maand = 1
    list = []

    while maand < 13 and dag < 31:
        list = []

        url = 'https://www.telegraaf.nl/archief/2020/' + str(maand) + '/' + str(dag)

        print(url)
        list = get_articles(url)
        export_articles(list)
        if dag < 28:
            dag += 1
        else:
            dag = 1
            maand += 1
