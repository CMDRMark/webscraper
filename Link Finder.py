import pickle
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# driver = webdriver.Chrome("/Users/arman1/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/chromedriver")
                          # , options=chrome_options) ###use these lines if you want to run this code without google chrome GUI

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15', 'accept': '*/*'}
HOST = 'https://mdk-arbat.ru'

with open('Links_mdk_cat', 'rb') as f:
    Dict = pickle.load(f)

def get_content(html):
    driver.get(html)
    driver.find_element(By.CSS_SELECTOR,
                        "#sort_and_qty > fieldset > div:nth-child(1) > span > select > option:nth-child(4)").click() #use this part if there is JS embeded and you want to interact with it before pulling the data
    
    WebDriverWait(driver, 3)
    driver.find_element(By.CSS_SELECTOR,
                        "#sort_and_qty > fieldset > div:nth-child(2) > span > select > option:nth-child(3)").click() #same hare
    WebDriverWait(driver, 7)
    for i in range(2, 21):
        print("Page number:", i-1 )
        source = driver.page_source  #after interaction with webpage transfer page source to BeautifulSoup and scrape it. It isn't nessesary bit for this particular occasion BS was much faster than Selenium
        soup = BeautifulSoup(source, 'html.parser')
        items = soup.find_all('div', class_='col-xs-6 col-sm-6 col-md-4 col-lg-3')
        for item in items:
            link = item.find('a', class_='tg-bookimg').get('href')
            global Links
            Links.append(HOST + str(link))
            print(len(Links))
        newlink = str(html) + "&pid=" + str(i)
        driver.get(newlink)

Links = []
for i in range(12, 49): 
    URL = Dict[i]['link']
    print(URL)
    filename = 'Links for', str(Dict[i]['genre'])
    driver = webdriver.Chrome("/Users/arman1/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/chromedriver")
    get_content(URL)
    file = open(str(filename), 'wb')
    pickle.dump(Links, file)
    file.close()
    print(len(Links))
    print(filename)
    Links = []
