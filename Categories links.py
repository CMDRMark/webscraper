from bs4 import BeautifulSoup
import pickle
import requests

URL = 'https://mdk-arbat.ru/catalog?subj_id=51'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15', 'accept': '*/*'}
HOST = 'https://mdk-arbat.ru'
Links = []

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    links=[]
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', style = 'padding-left:15px;')
    for item in items:
        link = item.find('a').get('href')
        genre = item.find('a')
        genre = genre.find('span').getText().strip()
        print (link,genre)
        global Links
        Links.append({
            'link': (HOST + str(link)),
            'genre': genre
        })


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')

parse(URL)
print (Links)

file = open("Links_mdk_cat", 'wb')
pickle.dump(Links, file)
file.close()
