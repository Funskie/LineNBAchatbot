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

line_bot_api = LineBotApi('WjlmNUqRQboB20VBmFDjIcQIX23i1m9USBL7atoIH52jWaJNiAMjTME4mLrhWY6cIO8YiKcTb4Lg7y86UWgyzmq44a3ccJbomwIBfLzE9KyZ6SgcNLf6cIQaLBbjaXj0HYdn+/xS5PPsNg8z0rWYcAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('62a8d88a917c14ac76ad6d510da67a4a')

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
    msg = msg.encode('utf-8')
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='57可愛'))

if __name__ == "__main__":
    app.run(debug=True,port=5700)
