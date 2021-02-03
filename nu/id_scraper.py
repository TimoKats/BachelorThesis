import requests

index = 6051009
source = ""

article_file = open('nu/articles.txt', 'a+')
ads_file = open('nu/ads.txt', 'a+')

while index < 7000000:
    url = 'https://www.nu.nl/advertorial/' + str(index)
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