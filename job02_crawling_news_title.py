from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from bs4 import BeautifulSoup  #pip install bs4
import requests #pip install requests
import time
import re
import pandas as pd
import datetime


category = ['Politics','Economic','Social','Culture','World','IT']
options = ChromeOptions()
user_agent = 'User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

pages = [105, 105, 105, 81, 105, 81]


df_titles = pd.DataFrame()

re_title = re.compile('[^가-힣|A-Z|a-z]')

for l in range(6):
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
    titles = []
    for k in range(1, pages[l]):
        url = section_url + '#date=%2000:00:00&page={}'.format(k)
        try:
            driver.get(url)
            time.sleep(0.5)
        except:
            print('driver.get',l,k)

        time.sleep(0.5)
        for i in range(1,5):
            for j in range(1,6):
                try:
                    title = driver.find_element('xpath','//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i,j)).text
                    title = re.compile('[^가-힣]').sub(' ',title)
                    titles.append(title)
                except:
                    print('find element',l,k,i,j)
        if k % 5 == 0:
            print(l,k)
            df_section_titles = pd.DataFrame(titles, columns=['title'])
            df_section_titles['category'] = category[l]
            df_section_titles.to_csv('./crawling_data/data_{}_{}.csv'.format(l,k))
        # df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

driver.close()

    # print(titles)
    # print(len(titles))


# df_titles.to_csv()


