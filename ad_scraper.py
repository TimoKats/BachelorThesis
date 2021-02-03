from bs4 import BeautifulSoup
import requests
import re

def clean_text(text):
    return text.replace(',', '')

def export_csv(source, id, date_published, date_modified, sponsor, title, introduction, body):
    output = open('data.csv', 'a', encoding='utf-8')
    output.write(source + ',' + id + ',' + date_published + ',' + date_modified + ',' + sponsor  + ',' + introduction + ',' + body + '\n')
    output.close()

class scraper:
    def __init__(self, id):
        self.url = "https://www.nu.nl/advertorial/" + id
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        self.text = self.soup.get_text()

    def get_url(self):
        return self.url.replace('\n', '')

    def get_title(self):
        index_1 = self.text.find('"headline": ')
        index_2 = self.text.find('\n', index_1)
        title = self.text[index_1+12:index_2-1]
        return clean_text(title)

    def get_sponsor(self):
        index_1 = self.text.find('"articleSection": [')
        index_2 = self.text.find('],', index_1)
        sponsor = self.text[index_1+28:index_2-4]
        return sponsor.replace('\n', '')

    def get_date_published(self):
        index_1 = self.text.find('"datePublished": ')
        index_2 = self.text.find('+', index_1)
        date = self.text[index_1+18:index_2]
        return date

    def get_date_modified(self):
        index_1 = self.text.find('"dateModified": ')
        index_2 = self.text.find('+', index_1)
        date = self.text[index_1+17:index_2]
        return date

    def get_introduction(self):
        index_1 = self.text.find('"description": ')
        index_2 = self.text.find('\n', index_1)
        introduction = self.text[index_1+15:index_2-1]
        return clean_text(introduction)

    def get_body(self):
        index_1 = self.text.find('"articleBody": ')
        index_2 = self.text.find('\n', index_1)
        body = self.text[index_1+15:index_2-1]
        return clean_text(body)

# zoek nog naar bug
if __name__ == '__main__':
    export_csv('source', 'article_id', 'date_published', 'date_modified', 'sponsor', 'title', 'introduction', 'body')
    with open('ads_test.txt', 'r+') as file_id:
        for id in file_id:
            if id is not "":
                str_id = str(id)
                id = scraper(str_id[:-1])
                if ((id.get_date_published() is not "") or (len(id.get_date_published()) > 50)):
                    export_csv('nu.nl', str_id[:-1], id.get_date_published(), id.get_date_modified(), id.get_sponsor(), id.get_title(), id.get_introduction(), id.get_body())