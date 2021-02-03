from bs4 import BeautifulSoup
import requests
import re

def get_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.find_all('a')
    return str(text)

def remove_duplicates(list):
    result = []
    for i in list:
        if i not in result and (len(i) < 100 and len(i) > 0):
            result.append(i)
    return result

def get_ads(sponsor, text):
    index_2 = 0
    count = 0
    ads = []
    while count < 50:
        index_1 = text.find('href="/gesponsord/', index_2)
        index_2 = text.find('">', index_1 + 1)
        ads.append(text[index_1+18:index_2])
        count += 1
    return remove_duplicates(ads)

def get_sponsors(text):
    index_2 = 0
    count = 0
    sponsors = []
    while count < 200:
        index_1 = text.find('href="/gesponsord/', index_2)
        index_2 = text.find('">', index_1 + 1)
        sponsors.append(text[index_1+18:index_2-1])
        count += 1
    return remove_duplicates(sponsors)

def export_ads(ad_list):
    file = open('ads.txt', 'a+')
    for ads in ad_list:
        for ad in ads:
            file.write(ad + '\n')
    return

if __name__ == '__main__':
    text_sponsors = get_text("https://www.telegraaf.nl/gesponsord/")
    sponsors = get_sponsors(text_sponsors)
    ad_list = []

    for sponsor in sponsors:
        text_ads = get_text('https://www.telegraaf.nl/gesponsord/' + sponsor + '/')
        ads = get_ads(sponsor, text_ads)
        ad_list.append(ads)

    export_ads(ad_list)