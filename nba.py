import re
import json
import time

import requests
from bs4 import BeautifulSoup

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR ChANNEL ACCESS TOKEN')
handler = WebhookHandler('CHANNEL SECRET')

def nba_links(math_list):
    content = ""
    for m in math_list:
        title = m['title']
        link = m['link']
        content += "{}\n{}\n".format(title, link)
    return content

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

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
       abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    # msg = msg.encode('utf-8')
    if msg == 'NBA':
        page = get_web_page('https://www.ptt.cc/bbs/NBA/index.html')

        if page:
            articles = []
            date = time.strftime("%m/%d")
            if date[0] == "0":
                date = date.replace("0", " ", 1)
            # print(date)
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
        # print(match)
        if len(match) > 0:
            c = nba_links(match)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=c))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入"NBA"查看今日LIVE直播連結'))

if __name__ == "__main__":
    app.run(debug=True,port=5700)