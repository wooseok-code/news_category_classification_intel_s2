from bs4 import BeautifulSoup  #pip install bs4

import requests #pip install requests

import re
import pandas as pd
import datetime

category = ['Politics','Economic','Social','Culture','World','IT']

# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
#
# # request를 거부할때 에러 대처법
# # header에다가 user agent정보를 담아서 보내주면 됨.
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
#
# resp = requests.get(url,headers=headers)
#
# print(resp)
# print(type(resp))
# #print(list(resp))
#
# soup = BeautifulSoup(resp.text, 'html.parser')
# #print(soup)
# title_tags = soup.select('.sh_text_headline') # sh_text_headline라는 클래스를 골라서 select해줌
#
# print(title_tags)
# print(len(title_tags))
# print(type(title_tags[0]))
# titles = []
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|A-Z|a-z]').sub(' ',title_tag.text)) # ^ : ~를 제외한것, -> 문자열이 아닌것을  ' '로 대체
#
# print(titles)

df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣|A-Z|a-z]')

for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url,headers=headers)
    soup = BeautifulSoup(resp.text,'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    for title_tag in title_tags:
        titles.append(re_title.sub(' ', title_tag.text))
    df_section_titles = pd.DataFrame(titles,columns=['title'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)









