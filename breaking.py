from config import TELEGRAM_TOKEN, CHAT_ID
import requests
from bs4 import BeautifulSoup
import time
import telegram
import re

bot = telegram.Bot(token=TELEGRAM_TOKEN)
delay = 300

daum_breaking_news_amount = 10
daum_news_amount = 10

naver_breaking_news_amount = 10
naver_news_amount = 10

lists = []
old_links = []

keyword = ["코로나", "코비드", "봉쇄", "확진", "감염", "속보"]

#max_length 최대길이 제한
def returns(url):
    req = requests.get(url)
    bs = BeautifulSoup(req.content, "html.parser")
    return bs

def daum_breaking_return_list(max_length):
    
    lists=[]

    bs = returns("https://news.daum.net/")
    div = bs.find("div", {"id":"kakaoContent"})
    li = div.findAll("li")

    length = 0

    for i in li:

        try:
            i.find("strong", {"class":"tit_thumb"})
            base = i.find("a")
            link = base['href']
            title = base.text
        except AttributeError:
            base = i.find("a")
            link = base['href']
            title = base.text
            pass

        try:
            title = base.text
        except AttributeError:
            img = base.find("img", {"class":"link_thumb"}).decompose()
            title = img.text

        if(link not in old_links):
            if("코로나" in title or "코비드" in title or "봉쇄" in title or "확진" in title or "감염" in title or "속보" in title):
                if(length == max_length):
                    return lists
                else:
                    lists.append([title, link])
                    old_links.append(link)
                    length+=1
                    #print(length)

    if(len(lists) != 0):
        return lists
    else:
        raise TypeError

def daum_return_list(max_length):
    
    lists=[]

    for j in range(len(keyword)):

        url = f'https://search.daum.net/search?w=news&sort=recency&q={keyword[j]}&cluster=n&DA=STC&dc=STC&pg=1&r=1&p=1&rc=1&at=more&sd=&ed=&period='
        bs = returns(url)
        li = bs.select("ul#newsResultUL > li .cont_inner")

        length = 0

        for i in li:

            base = i.find("a")
            title = base.text
            desc = i.text

            link = base['href']

            if(link not in old_links):
                if("코로나" in title or "코비드" in title or "봉쇄" in title or "확진" in title or "감염" in title or "전염" in title or "속보" in title):
                    if(length == max_length):
                        return lists
                    else: 
                        lists.append([title, link])
                        old_links.append(link)
                        length+=1
                else:
                    if("코로나" in desc or "코비드" in desc or "봉쇄" in desc or "확진" in desc or "감염" in desc or "전염" in desc or "속보" in desc):
                        if(length == max_length):
                            return lists
                        else: 
                            lists.append([title, link])
                            old_links.append(link)
                            length+=1
                            #print(length)
                    else:
                        lists.append([title, link])
                        old_links.append(link)
                        length+=1

        if(len(lists) != 0):
            return lists
        else:
            raise TypeError

def naver_breaking_return_list(max_length):
    
    lists=[]

    bs = returns("https://news.naver.com/main/home.nhn")
    td = bs.find("div", {"id":"container"})
    li = td.findAll("li")

    length = 0
    for i in li:
        try:
            i.find("dt", {"class":"photo"}).decompose()
        except AttributeError:
            pass

        base = i.find("a")
        title = base.text

        link = base['href']

        if(link not in old_links):
            if("코로나" in title or "코비드" in title or "봉쇄" in title or "확진" in title or "감염" in title or "전염" in title or "속보" in title):
                if(length == max_length):
                    return lists
                else:
                    lists.append([title, link])
                    old_links.append(link)
                    length+=1

    if(len(lists) != 0):
        return lists
    else:
        raise TypeError



def naver_return_list(max_length):
    
    lists=[]

    for j in range(len(keyword)):

        url = f'https://search.naver.com/search.naver?where=news&query={keyword[j]}&sm=tab_srt&sort=1&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&mynews=0&refresh_start=0&related=0'
        bs = returns(url)
        li = bs.select("ul.type01 > li")

        length = 0

        for i in li:
            base = i.find("dl").find("a")
            title = base.text

            try:
                i.find("dd", {"class":"txt_inline"}).decompose()
            except AttributeError:
                pass

            desc = i.find("dd").text
            link = base['href']

            if(link not in old_links):
                if("코로나" in title or "코비드" in title or "봉쇄" in title or "확진" in title or "감염" in title or "전염" in title or "속보" in title):
                    if(length == max_length):
                        return lists
                    else: 
                        lists.append([title, link])
                        old_links.append(link)
                        length+=1
                else:
                    if("코로나" in desc or "코비드" in desc or "봉쇄" in desc or "확진" in desc or "감염" in desc or "전염" in desc or "속보" in desc):
                        if(length == max_length):
                            return lists
                        else: 
                            lists.append([title, link])
                            old_links.append(link)
                            length+=1
                            #print(length)
                    else:
                        lists.append([title, link])
                        old_links.append(link)
                        length+=1

        if(len(lists) != 0):
            return lists
        else:
            raise TypeError

def message(i):
    title = i[0].replace("\r", "")
    title = i[0].replace("\n", "")
    title = i[0].replace("\t", "")
    bot.sendMessage(CHAT_ID, "{}\n{}".format(title, i[1]))
    print("{}\n{}".format(i[0], i[1]))
    time.sleep(delay)

def sendBots():
    try:
        print("Start 1 -----------------------------------------------------------------------------------------------------")

        lists = daum_breaking_return_list(daum_breaking_news_amount)
        for i in lists:
            #bot.sendMessage로 대체
            message(i)

    except TypeError:
        print("Error 1")

    print("End 1 -----------------------------------------------------------------------------------------------------")

    try:
        print("Start 2 -----------------------------------------------------------------------------------------------------")

        lists = daum_return_list(daum_news_amount)
        for i in lists:
            #bot.sendMessage로 대체
            message(i)

    except TypeError:
        print("Error 2")

    print("End 2 -----------------------------------------------------------------------------------------------------")

    try:
        print("Start 3 -----------------------------------------------------------------------------------------------------")

        lists = naver_breaking_return_list(naver_breaking_news_amount)
#        print(lists)
        for i in lists:
            #bot.sendMessage로 대체
            message(i)

    except TypeError:
        print("Error 3")

    print("End 3 -----------------------------------------------------------------------------------------------------")

    try:
        print("Start 4 -----------------------------------------------------------------------------------------------------")

        lists = naver_return_list(naver_news_amount)
#        print(lists)
        for i in lists:
            #bot.sendMessage로 대체
            message(i)

    except TypeError:
        print("Error 4")

    print("End 4 -----------------------------------------------------------------------------------------------------")

sendBots()