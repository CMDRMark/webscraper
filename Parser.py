# -*- coding: utf-8 -*-
import pickle
import itertools
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


file_name_cat = ['Биология', 'Военное дело', 'Горная промышленность', 'Государство и право', 'Книги для детей и подростков', 'Дом. Досуг. Хобби', 'Естественные науки в целом', 'Жилищно-коммунальное хозяйство. Бытовое обслуживание', 'Здравоохранение. Медицина', 'Искусство', 'Использование атомной энергии. Ядерная техника', 'История', 'Космос', 'Культура. Библиотечное дело. Музееведение', 'Легкая промышленность', 'Лесная, деревообрабатывающая, лесохимическая, целлюлозно-бумажная промышленность', 'Лесное хозяйство. Водное хозяйство.Рыбное хозяйство', 'Литература универсального содержания', 'Машиностроение. Приборостроение', 'Металлургия', 'Наука. Науковедение. Кибернетика. Семиотика. Информатика', 'Науки о земле', 'Некнижные товары', 'Образование. Учебная литература', 'Общественные науки в целом. Социология', 'Пищевая промышленность', 'Полиграфия. Репрография. Кинофототехника', 'Политика', 'Промышленность в целом', 'Психология', 'Радиоэлектроника. Связь', 'Сельское хозяйство', 'Средства массовой информации', 'Демография. Статистика', 'Строительство','Технические науки', 'Транспорт','Путешествия. Карты', 'Физико-математические науки', 'Физическая культура. Спорт', 'Филологические науки', 'Философия и религия', 'Химическая промышленность', 'Химия', 'Художественная литература', 'Эзотерика. Самопознание',
                 'Бизнес и финансы', 'Энергетика']
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome("/Users/arman1/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/chromedriver", options=chrome_options)
BOOKS = []
def get_content(html):

    global BOOKS
    driver.get(html)
    switch = True
    try:
        title = driver.find_element(By.XPATH, '//*[@id="tg-content"]/div[2]/div[1]/div[2]/div[1]/h1').text.strip()
    except:
        switch = False
    if switch == True:
        try:
            author = driver.find_element(By.XPATH, '//*[@id="tg-content"]/div[2]/div[1]/div[2]/div[1]/span/a').text.strip()
        except:
            author = "Автор не указан"
        try:
            pub = driver.find_element(By.XPATH, "//*[text()='Издательство:']//parent::li")
            publisher = pub.find_element(By.XPATH, '//*[@id="description"]/div/ul/li[6]/span[2]').text.strip()
        except:
            publisher = "Издатель не указан"
        genre = driver.find_element(By.XPATH, '//*[@id="tg-content"]/div[1]/span/a').text.strip()
        BOOKS.append({
            'title': title,
            'author': author,
            'genre': genre,
            'publisher': publisher
        })
        print(len(BOOKS))
    else:
        pass
def save_file(items, path):
    with open(path, 'w+', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Автор', 'Жанр', 'Издательство'])
        for item in items:
            writer.writerow([item['title'], item['author'], item['genre'], item['publisher']])

for block in itertools.islice(file_name_cat, 35, 49):
    each_dict = ("('Links for', '" + str(block) + "')")
    with open(str(each_dict) ,'rb') as f:
        URL = pickle.load(f)
    print (URL)
    print(len(URL))
    full_files = (len(URL)-1)//250
    half_files = (len(URL)-1)%250
    print( "Full files:" + str(full_files))
    print("In last file:" + str(half_files))
    a = 0
    b = a + 250
    if full_files == 0:
        for line in itertools.islice(URL, 0, len(URL)):
            print(line)
            get_content(line)
            print("1 file", len(BOOKS))
        FILE = str(block) + ".csv"
        save_file(BOOKS, FILE)
        BOOKS = []
    else:
        for i in range(1, full_files+1):
            for line in itertools.islice(URL, a, b):
                print(line)
                get_content(line)
                print( str(i) + " file", len(BOOKS))
            FILE = str(block) + str(2022- i) + ".csv"
            save_file(BOOKS, FILE)
            BOOKS = []
            if i != full_files:
                a +=250
                b += 250
        for line in itertools.islice(URL, b, len(URL)):
            print(line)
            get_content(line)
            print("1 file", len(BOOKS))
        FILE = str(block) + "_last.csv"
        save_file(BOOKS, FILE)
        BOOKS = []