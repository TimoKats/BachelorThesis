# speed and power...solves many many things. -Jeremy Clarkson
# name:         url_scraper_nu.py
# author:       Timo Kats
# last update:  20/05/2021
# description:  Brute force scraping algorithm for nu.nl. See algorithm 1 in thesis.

import requests

index = 0
source = ""

article_file = open('nu/articles.txt', 'a+')
ads_file = open('nu/ads.txt', 'a+')

while True:
    url = 'https://www.nu.nl/algemeen/' + str(index)
    request = requests.get(url)
    print("currently at index: ", index)
    if request.status_code == 200:
        source = request.text
        if("Dit is een gesponsord artikel op NU.nl" in source):
            ads_file.write(str(index) + '\n')
            ads_file.flush()
        else:
            article_file.write(str(index) + '\n')
            article_file.flush()
    index += 1
