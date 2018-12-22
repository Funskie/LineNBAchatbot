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

line_bot_api = LineBotApi('RVQm6gRK1rqc9e3E6bwI/3BwrMhFgIECXzRwIjj0oHVOsuCbj1osmWjh+9pGlt/0IO8YiKcTb4Lg7y86UWgyzmq44a3ccJbomwIBfLzE9KzQ7UoFj/3RIix0NnHt4Wf86/dBtfXcdVuU74gCYn2bkgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4964336f77ad4b20de39cff3ea7dc4ff')

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
