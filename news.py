# 라이브러리 불러오기
from config import TELEGRAM_TOKEN, CHAT_ID
from noti import news
import requests
from bs4 import BeautifulSoup
import telegram

bot = telegram.Bot(token=TELEGRAM_TOKEN)
# 서치 키워드
search_word = '코로나'
# 기존에 보냈던 링크를 담아둘 리스트
naver_old_links = []
naver_old_titles = []

daum_old_links = []
daum_old_title = []

# 스크래핑 함수 
def naver_extract_links(old_links=[]):
    naver_url = f'http://search.naver.com/search.naver?where=news&sm=tab_jum&query={search_word}&nso=p%3Aall%2Cso%3Add'
    naver_req = requests.get(naver_url)
    naver_html = naver_req.text
    naver_soup = BeautifulSoup(naver_html, 'html.parser')

    naver_search_result = naver_soup.select_one('.type01')
    naver_news_list = naver_search_result.select('li a')

    naver_links = []
    for naver_news in naver_news_list[:10]:
        naver_link = naver_news['href']
        naver_links.append(naver_link)

    naver_new_links = []
    for naver_link in naver_links:
        if naver_link not in naver_old_links:
           naver_new_links.append(naver_link)

#    naver_titles = []
#    for naver_news_title in naver_news_list[:10]:
#        naver_title = naver_news_title['title']
#        naver_titles.append(naver_title)

#    naver_new_titles=[]
#    for naver_title in naver_titles:
#        if naver_title not in naver_old_links:
#           naver_new_titles.append(naver_title)

    return naver_new_links
#   return naver_new_titles

# 스크래핑 함수 
def daum_extract_links(old_links=[]):
    daum_url = f'http://search.daum.net/search?w=news&sort=recency&q={search_word}&cluster=n&DA=STC&dc=STC&pg=1&r=1&p=1&rc=1&at=more&sd=20200326210541&ed=20200327210541&period=d'
    daum_req = requests.get(daum_url)
    daum_html = daum_req.text
    daum_soup = BeautifulSoup(daum_html, 'html.parser')

    daum_search_result = daum_soup.select_one('#newsResultUL')
    daum_news_list = daum_search_result.select('li a')

    daum_links = []
    for daum_news in daum_news_list[:10]:
        daum_link = daum_news['href']
        daum_links.append(daum_link)

    daum_new_links = []
    for daum_link in daum_links:
        if daum_link not in daum_old_links:
           daum_new_links.append(daum_link)

#    daum_titles = []
#    for daum_news_title in daum_news_list[:10]:
#        daum_title = daum_news_title['title']
#        daum_titles.append(daum_title)

#    daum_new_titles=[]
#   for daum_title in daum_titles:
#        if daum_title not in daum_old_links:
#           daum_new_titles.append(daum_title)
    
    return daum_new_links
#    return daum_new_titles


# 이전 링크를 매개변수로 받아서, 비교 후 새로운 링크만 출력
# 차후 이 부분을 메시지 전송 코드로 변경하고 매시간 동작하도록 설정
# 새로운 링크가 없다면 빈 리스트 반환
for i in range(10):
    naver_new_links = naver_extract_links(naver_old_links)
    naver_old_links += naver_new_links.copy()
    naver_old_links = list(set(naver_old_links))

#    naver_new_titles = naver_extract_links(naver_old_links)
#    naver_old_titles += naver_new_titles.copy()
#    naver_old_titles = list(set(naver_old_links))

#    naver_news = naver_new_titles[i] + '\n\n' + naver_new_links[i]
    
    bot.sendMessage(CHAT_ID, i[i])


for i in range(10):
    daum_new_links = daum_extract_links(daum_old_links)
    daum_new_links += daum_new_links.copy()
    daum_new_links = list(set(daum_old_links))

#    daum_new_titles = naver_extract_links(daum_old_links)
#    daum_old_titles += daum_new_titles.copy()
#    daum_old_titles = list(set(daum_old_links))
    
#    daum_news = daum_new_titles[i] + '\n\n' + daum_new_links[i]
    
    bot.sendMessage(CHAT_ID, i[i])


"""
===보낼 링크===
 ['https://m.news.naver.com/read.nhn?mode=LSD&mid=sec&sid1=101&oid=008&aid=0004349743', 'http://it.chosun.com/site/data/html_dir/2020/01/31/2020013103216.html', 'https://m.news.naver.com/read.nhn?mode=LSD&mid=sec&sid1=101&oid=031&aid=0000523810', 'https://m.news.naver.com/read.nhn?mode=LSD&mid=sec&sid1=102&oid=001&aid=0011371561', 'http://www.fintechpost.co.kr/news/articleView.html?idxno=100097'] 

===보낼 링크===
 [] 

===보낼 링크===
 [] 
"""

