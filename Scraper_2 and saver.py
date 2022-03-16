import pickle
import itertools
import csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
chrome_options = Options()

BOOKS = []
file_name_cat = ['Классическая литература','Современная проза','Отечественные','Зарубежные','Иронические детективы','Отечественная фантастика','Зарубежная фантастика','Отечественное фэнтези','Зарубежное фэнтези','Ужасы','Фантастический боевик','Российские','Зарубежные','Исторические','Поэзия','Драматургия','Публицистика','Биографии','Мемуары','Хроники событий. Дневники','Исторические романы','Приключения','Комиксы и манга','Юмор','Афоризмы. цитаты','Мифы. Легенды. Эпос','Сказки',
                 'Пословицы. Поговорки. Загадки','Прочие издания']

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome("/PATH TO chromedriver", options=chrome_options)

def get_content(html):
    global BOOKS
    driver.get(html)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.collapsed"))).click() #Waiting for JS interaction, after which 
        #object becomes interractable to reveal more content
        
        title = driver.find_element(By.XPATH, '//*[@id="productMain"]/div[2]/div/p[1]/following-sibling::h1').text.strip()
        author = driver.find_element(By.XPATH, '//*[@id="productMain"]/div[2]/div/p[1]/a').text.strip()
        genre = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/nav/ol/li[2]/a').text.strip()
        try:
            publisher = (driver.execute_script('return arguments[0].lastChild.textContent;',
                                               WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Издатель:']//ancestor::td[1]")))).strip())
        except:
            publisher = "Издатель не указан"
        BOOKS.append({
            'title': title,
            'author': author,
            'genre': genre,
            'publisher': publisher
        })
        print(title, author, publisher, genre)
    except:
        print('Пропуск строки')
        print(len(BOOKS))

def save_file(items, path):
    with open(path, 'w+', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Автор', 'Жанр', 'Издательство'])
        for item in items:
            writer.writerow([item['title'], item['author'], item['genre'], item['publisher']])

for block in itertools.islice(file_name_cat, 26, 29):
    each_dict = ("BG/('Links for', '" + str(block) + "')")
    print(block)
    print(each_dict)
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
