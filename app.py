#===== import LineBot SDK相關套件 =====
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import * 
#===== import LineBot SDK相關套件 =====

import re # 字串處理模組
from flask import Flask, request, abort # 網頁框架套件
from Lotto import * # 樂透爬蟲程式
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

# Line Developers → Messaging API → Channel access token 
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

# Line Developers → Basic settings → Channel secret
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# Line Developers → Basic settings → Your user ID and 想要顯示的TextSendMessage
line_bot_api.push_message(config.get('line-bot', 'user_id'), TextSendMessage(text="Hi，這是肥肥樂透!")) # 主動push message


# HEROKU(雲端服務) 串接 Line Developers(Line管理平台) 
# HEROKU → Deploy → Open app 複製URL → Line Developers → Messaging API → Webhook URL 貼上+"/callback"
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] # get X-Line-Signature header value 
    body = request.get_data(as_text=True) # get request body as text
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#===== call Lotto 樂透爬蟲 Function =====
BigResult = Lotto("Big")
AyaResult = Lotto("Aya")
PowerResult = Lotto("Power")
#===== call Lotto 樂透爬蟲 Function =====


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event): # event事件(使用者作的事件)
    message = event.message.text
    # 肥肥樂透
    if re.match('肥肥樂透', message):
        carousel_template_message = TemplateSendMessage(
        alt_text = "肥肥樂透",
        template = CarouselTemplate(
            columns=
            [
                CarouselColumn # 樂透爬蟲
                (
                    thumbnail_image_url = "https://i.imgur.com/tG3ZSkc.jpg",
                    title = "請選擇「樂透種類」",
                    text = "查詢樂透",
                    actions = 
                    [
                        MessageAction(
                            label = "大樂透",
                            text = "查詢大樂透"
                        ),
                        MessageAction(
                            label = "今彩539",
                            text = "查詢今彩539",
                        ),
                        MessageAction(
                            label = "威力彩",
                            text = "查詢威力彩",
                        )
                    ]
                ),
                CarouselColumn # 電腦選號
                (
                    thumbnail_image_url = "https://i.imgur.com/tG3ZSkc.jpg",
                    title = "請選擇「樂透種類」",
                    text = "電腦選號",
                    actions = 
                    [
                        MessageAction(
                            label = "大樂透電腦選號",
                            text = "大樂透電腦選號"
                        ),
                        MessageAction(
                            label = "威力彩電腦選號",
                            text = "威力彩電腦選號",
                        ),
                        MessageAction(
                            label = "今彩539電腦選號",
                            text = "今彩539電腦選號",
                        )
                    ]
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    elif re.match("查詢大樂透", message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(BigResult))
    elif re.match("查詢今彩539", message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(AyaResult))
    elif re.match("查詢威力彩", message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(PowerResult))
    elif re.match("大樂透電腦選號", message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("大樂透電腦選號： \n" + RandomLotto("Big")))
    elif re.match("威力彩電腦選號", message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("威力彩電腦選號： \n" + RandomLotto("Power")))
    elif re.match("今彩539電腦選號", message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("今彩539電腦選號： \n" + RandomLotto("Aya")))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入「肥肥樂透」"))


# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) # 0.0.0.0 全世界的ip都可以用該機器人