import re
import json
import time

import requests
from bs4 import BeautifulSoup

def notification(title, link):
    content = "{}\n{}".format(title, link)
    line_bot_api.multicast(notify_list, TextSendMessage(text=content))
    return True

def get_web_page(link):
    time.sleep(0.5)
    res = requests.get(link, cookies={'over18': '1'})
    if res.status_code != 200:
        print('Invalid url: ', res.url)
        return None
    else:
        return res.text

def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')
    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = 'https://www.ptt.cc' + paging_div.find_all('a')[1]['href']

    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').string == date:  # 發文日期正確
            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').string
                link = 'https://www.ptt.cc' + href
                articles.append({'title':title, 'link':link})
    return articles, prev_url

page = get_web_page('https://www.ptt.cc/bbs/NBA/index.html')

if page:
    articles = []
    date = time.strftime("%m/%d").lstrip('0')
    current_articles, prev_url = get_articles(page, date)
    while current_articles:
        articles += current_articles
        page = get_web_page(prev_url)
        current_articles, prev_url = get_articles(page, date)

    re_gs_title = re.compile(r'^\[Live\]', re.I)

    match = []
    for article in articles:
        title = article['title']
        if re_gs_title.match(title) != None:
            link = article['link']
            match.append({'title':title, 'link':link})
print(match)
# if len(match) > 0:
#     with open('data/history/gamesale.json', 'r+') as file:
#         history = json.load(file)

#         now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         new_flag = False
#         for article in match:
#             if article['id'] in history:
#                 continue
#             new_flag = True
#             history.append(article['id'])
#             notification(article['title'], article['link'])
#             print("{}: New Article: {} {}".format(now, article['title'], article['link']))

#         if new_flag == True:
#             file.seek(0)
#             file.truncate()
#             file.write(json.dumps(history))
#         else:
#             print("{}: Nothing".format(now))