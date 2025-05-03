from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
# openai.api_key = os.getenv('OPENAI_API_KEY')


def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def Carousel_mlb():
    message = TemplateSendMessage(
        alt_text='首頁',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/LA_Dodgers.svg/500px-LA_Dodgers.svg.png",
                    title='洛杉磯道奇隊',
                    text='球隊官網',
                    actions=[
                        URITemplateAction(
                            label="進入頁面",
                            uri="https://www.mlb.com/dodgers/"
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/NewYorkYankees_caplogo.svg/250px-NewYorkYankees_caplogo.svg.png',
                    title='紐約洋基隊',
                    text='球隊官網',
                    actions=[
                        URITemplateAction(
                            label="進入頁面",
                            uri="https://www.mlb.com/yankees/"
                        )
                    ]
                )
            ]
        )
    )
    return message

def Carousel_japan():
    message = TemplateSendMessage(
        alt_text='首頁',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Hokkaido_Nippon-Ham_Fighters_insignia.png",
                    title='北海道日本火腿鬥士隊',
                    text='球隊官網',
                    actions=[
                        URITemplateAction(
                            label="進入頁面",
                            uri="https://www.fighters.co.jp/global/taiwanese/"
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Hanshin_tigers_insignia.PNG/500px-Hanshin_tigers_insignia.PNG',
                    title='阪神虎隊',
                    text='球隊官網',
                    actions=[
                        URITemplateAction(
                            label="進入頁面",
                            uri="https://hanshintigers.jp/"
                        )
                    ]
                )
            ]
        )
    )
    return message

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '美國' in msg and '戰績' in msg :
        message = TextSendMessage(text="https://tw.sports.yahoo.com/mlb/standings/")
        line_bot_api.reply_message(event.reply_token, message)
    elif '美國' in msg and '球員' in msg :
        message = TextSendMessage(text="https://tw.sports.yahoo.com/mlb/teams/")
        line_bot_api.reply_message(event.reply_token, message)
    elif '美國' in msg and '球隊' in msg :
        message = Carousel_mlb()
        line_bot_api.reply_message(event.reply_token, message)  
    elif '美國' in msg :
        message = TextSendMessage(text="https://tw.sports.yahoo.com/mlb/scoreboard/")
        line_bot_api.reply_message(event.reply_token, message)
    elif '日本' in msg and '戰績' in msg :
        message = TextSendMessage(text="https://www.fengyuncai.com/npb/standings.asp")
        line_bot_api.reply_message(event.reply_token, message)
    elif '日本' in msg and '球隊' in msg :
        message = Carousel_japan()
        line_bot_api.reply_message(event.reply_token, message)  
    elif '日本' in msg :
        message = TextSendMessage(text="https://www.msn.com/zh-tw/sports/baseball/npb")
        line_bot_api.reply_message(event.reply_token, message)
    elif '中華' in msg and '球員' in msg :
        message = TextSendMessage(text="https://www.cpbl.com.tw/player")
        line_bot_api.reply_message(event.reply_token, message)
    elif '中華' in msg :
        message = TextSendMessage(text="https://www.cpbl.com.tw/")
        line_bot_api.reply_message(event.reply_token, message)  
    else:
         message = TextSendMessage(text=msg)
         line_bot_api.reply_message(event.reply_token, message)

#
#    try:
#        GPT_answer = GPT_response(msg)
#        print(GPT_answer)
#        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
#    except:
#        print(traceback.format_exc())
#        line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))


@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
