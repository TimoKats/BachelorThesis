# speed and power...solves many many things. -Jeremy Clarkson
# name:         page_scraper_telegraaf.py
# author:       Timo Kats
# last update:  20/05/2021
# description:  Scrapes the content of a page. Uses the urls from the url scraper as input. See algorithm 3 in thesis.

from bs4 import BeautifulSoup
import requests
import re

def clean_text(text):
    return text.replace(',', '')

def export_csv(source, date_published, date_modified, sponsor, title, introduction, body):
    output = open('data.csv', 'a', encoding='utf-8')
    output.write(source + ',' + date_published + ',' + date_modified + ',' + sponsor + ',' + title + ',' + introduction + ',' + body + '\n')
    output.close()

class scraper:
    def __init__(self, id):
        self.id = id
        self.url = "https://www.telegraaf.nl/gesponsord/" + id
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.text = self.soup.get_text()
        self.text_2 = self.soup.get_text()

        for line in self.text.splitlines():
            if '"@type":"NewsArticle"' in line:
                self.text = line

    def get_id(self):
        index_1 = self.id.find('/')
        return self.id[:index_1]

    def get_url(self):
        return self.url.replace('\n', '')

    def get_title(self):
        index_1 = self.text.find('"headline":"')
        index_2 = self.text.find('",', index_1)
        title = self.text[index_1+11:index_2+1]
        return title

    def get_sponsor(self):
        return '"none"'

    def get_date_published(self):
        index_1 = self.text.find('"datePublished":')
        index_2 = self.text.find('.', index_1)
        date = self.text[index_1+17:index_2]
        return date

    def get_date_modified(self):
        index_1 = self.text.find('"dateModified":')
        index_2 = self.text.find('.', index_1)
        date = self.text[index_1+16:index_2]
        return date

    def get_introduction(self):
        index_1 = self.text.find('"description":')
        index_2 = self.text.find('",', index_1)
        intro = self.text[index_1+14:index_2+1]
        return clean_text(clean_text(intro))

    def get_body(self):
        index_1 = self.text.find('"articleBody":')
        index_2 = self.text.find('",', index_1)
        body = self.text[index_1+14:index_2+1]
        if len(body) > 200:
            return clean_text(body.replace('\\n', ' '))
        else:
            return " "

if __name__ == '__main__':
    export_csv('source', 'date_published', 'date_modified', 'sponsor', 'title', 'introduction', 'body')
    with open('articles_2.txt', 'r+') as file_id:
        for id in file_id:
            if id is not "":
                str_id = str(id)
                id = scraper(str_id)
                if(len(id.get_date_published()) < 50) and not("articleBody" in id.get_body()):
                    export_csv('telegraaf', id.get_date_published(), id.get_date_modified(), id.get_sponsor(),id.get_title(), id.get_introduction(), id.get_body())
