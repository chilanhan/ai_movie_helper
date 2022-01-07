import os.path
import tempfile
import json
import requests
from flask import Flask
app = Flask(__name__)

from flask import request, abort,render_template
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError

from linebot.models import *
from urllib.parse import parse_qsl
import datetime

from face_detecton.get_ten_pics_and_features import get_ten_pics_and_features,picture_to_vector_json
from mysql_package.yahoodata_cv2_to_mysql import yahoo_mysql_to_carousel,yahoo_csv_to_mysql
from mysql_package.mysql_insert import insert_user_to_mysql,insert_bookingdata_to_mysql,insert_ratingdata_to_mysql,insert_user_habit
from json_data.update_json_from_mysql import update_all_json


yc_token='6LtqwU4k493Gys589ikza9GzxWgrHjJFIcDGc21+JcMAALUjLd2xLzGRJft575QbIOeaUEedDr6QMf4mormSu0bCA8QuUTGj0kC0Im1qNsovhsMLv8tHwJjE2PkLvA44E8ckPuLRtWlTu3sNq+rNmwdB04t89/1O/w1cDnyilFU='
yc_secret='62fedcb34c8415668774fd2ccdb5d73c'

sy_token='2IT+lGbqil5lJCuY8ijAtLswcNi3sShNWPLoBOxNzo3iwm5Ob+8JyNsymS9WQCsKYp7YEhtTAIC2+C2Dm2sMvztIsDoKAaYXDUKxfh6OkpqmObF0eK2+ebunvj4IWw/OiS0eac9a6eJXp1c+y7b3wAdB04t89/1O/w1cDnyilFU='
sy_secret='d91f9849821716b3500eb7686daf3f8b'


HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {sy_token}'
}

booking_liffid='1656658324-yQ56DDov'
rating_liffid='1656658324-7ddvPPk0'
user_data_liffid='1656658324-ydPdBBDr'


line_bot_api = LineBotApi(sy_token)
handler = WebhookHandler(sy_secret)
dirpath=os.path.join(app.root_path,'\\resources')
print(dirpath)

@app.route('/booking_page')
def booking_page():
	return render_template('booking_page.html', liffid = booking_liffid)

@app.route('/rating_page')
def rating_page():
	return render_template('rating_page.html', liffid = rating_liffid)

@app.route('/user_data_page')
def user_data_page():
	return render_template('user_data.html', liffid = user_data_liffid)


def replyMessage(payload):
    response = requests.post('https://api.line.me/v2/bot/message/reply',
                             headers=HEADER, data=json.dumps(payload))
    #print(response.text)
    return 'OK'


#下載document
from flask import send_from_directory


@app.route('/downloads_json')

def download():
    filename = "user_face_info.json"
    dirpath=app.root_path

    return send_from_directory(dirpath,filename,as_attachment=True)

########################Index###################################
########################Index###################################

@app.route("/", methods=['POST'])
def index():
    body = request.json
    events = body["events"]
    print(events)
    if "replyToken" in events[0]:
        userid = events[0]["source"]["userId"]
        profile = line_bot_api.get_profile(str(userid))
        username = profile.display_name
        print(userid, username)
        insert_user_to_mysql(userid, username)
        payload = dict()
        replyToken = events[0]["replyToken"]
        print(replyToken)
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                mtext = events[0]["message"]["text"]

                if mtext == '@電影簡介':
                    update_all_json()
                    FlexMessage = json.load(open('json_data/mvlist.json', 'r', encoding='utf-8'))

                    payload["messages"]=[{
                        "type": "flex",
                        "altText": "This is a Flex Message",
                        "contents":FlexMessage
                      }]
                    replyMessage(payload)

                    #line_bot_api.reply_message(event.reply_token, FlexSendMessage('即將上映 /熱映電影清單', FlexMessage))

                elif mtext == '@電影推薦系統':
                    sendCarousel(event)

                elif mtext == '@論壇熱門話題':
                    ptt_check(events[0],replyToken)




                elif mtext == '@會員註冊':
                    personal(events[0],replyToken)


                elif mtext[:5] == '電影評分:' and len(mtext) > 6:
                    manage_rating_Form(mtext[5:],username)
                    payload["messages"]=[{
                        "type": "text",
                        "text":"評分成功!（重複輸入將覆蓋先前資料!）"
                      }]
                    replyMessage(payload)
                elif mtext[:10] == '喜歡電影和電影類型:' :
                    manage_user_habit_Form(mtext[10:],username)
                    payload["messages"]=[{
                        "type": "text",
                        "text":"偏好設定成功！（重複輸入將覆蓋先前資料!）"
                      }]
                    replyMessage(payload)

                elif mtext[:5] == '訂票資訊:':
                    print("in booking form")
                    manage_booking_Form(mtext[5:],username)
                    payload["messages"]=[{
                        "type": "text",
                        "text":"訂票成功！"
                      }]
                    replyMessage(payload)
                elif mtext[:3] == '///' and len(mtext) > 3:
                    manage_booking_Form(mtext, username)
            elif events[0]["message"]["type"]  == "video":
                handle_content_message(events[0],replyToken,userid,username)


        elif events[0]["type"] == "postback":
            data = events[0]["postback"]["data"]
            action = str(data).split("=")[1]
            print(action)

            if action.__contains__('movie'):
                if action == 'movie_rank1':
                    FlexMessage = json.load(open('json_data/on_movie1.json', 'r', encoding='utf-8'))

                elif action == 'movie_rank2':
                    FlexMessage = json.load(open('json_data/on_movie2.json', 'r', encoding='utf-8'))

                elif action == 'on_movie1':
                    FlexMessage = json.load(open('json_data/on_movie1.json', 'r', encoding='utf-8'))
                elif action == 'on_movie2':
                    FlexMessage = json.load(open('json_data/on_movie2.json', 'r', encoding='utf-8'))
                elif action == 'on_movie3':
                    FlexMessage = json.load(open('json_data/on_movie3.json', 'r', encoding='utf-8'))
                elif action == 'coming_movie1':
                    FlexMessage = json.load(open('json_data/coming_movie1.json', 'r', encoding='utf-8'))
                elif action == 'coming_movie2':
                    FlexMessage = json.load(open('json_data/coming_movie2.json', 'r', encoding='utf-8'))
                elif action == 'coming_movie3':
                    FlexMessage = json.load(open('json_data/coming_movie3.json', 'r', encoding='utf-8'))
                payload["messages"] = [{
                    "type": "flex",
                    "altText": "電影簡介",
                    "contents": FlexMessage
                }]
                replyMessage(payload)

            else:
                if action == 'open_camera':
                    user_camera_open(events[0],replyToken)



    return 'OK'



########################Index###################################
########################Index###################################

########################callbaok###################################
########################callback###################################

@app.route("/callback", methods=['POST'])

def callback():
    body = request.json
    events = body["events"]
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

########################callbaok###################################
########################callback###################################



########################MessageEvent###################################
########################MessageEvent###################################

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    userid = event.source.user_id
    profile = line_bot_api.get_profile(str(userid))
    username=profile.display_name
    print(userid,username)

    insert_user_to_mysql(userid,username)




########################MessageEvent###################################
########################MessageEvent###################################


#儲存影片
#@handler.add(MessageEvent,message=(VideoMessage))
def handle_content_message(event,replyToken,userid,username):

    print(event)
    static_tmp_path='./resources'
    #print(event)
    message_content=line_bot_api.get_message_content(event["message"]["id"])
    with tempfile.NamedTemporaryFile(dir=static_tmp_path,prefix=username+'___',delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path=tf.name

    dist_path=tempfile_path+'.mp4'
    dist_name=os.path.basename(dist_path)
    os.rename(tempfile_path,dist_path)
    print('./resources/'+dist_name)

    #face detection
    get_ten_pics_and_features('./resources/'+dist_name,username)


    message = TextSendMessage( text='成功搜集人臉特徵')
    line_bot_api.reply_message( replyToken, message)


    #face vector into  json
    picture_to_vector_json()

    # line_bot_api.reply_message(
    #     replyToken,[
    #         TextSendMessage(text='成功搜集人臉特徵'),
    #         TextSendMessage(text=dist_name),
    #
    #     ])

    # payload = dict()
    # payload["replyToken"] = reply_token
    # payload["messages"] = [{
    #     "type": "text",
    #     "text": "成功搜集人臉特徵"
    # }]
    # replyMessage(payload)


    # line_bot_api.reply_message(
    #     reply_token,
    #         TextSendMessage(text='成功搜集人臉特徵') )







def user_camera_open(event,reply_token):
    queries = ConfirmTemplate(
        text="人臉註冊請錄製5秒以上的影片上傳，請問是否開啟相機?",
        actions=[
            URIAction(
                label='開啟相機',
                uri='line://nv/camera'
            ),
            MessageAction(label='不需要', text='不需要')

        ])

    temp_msg = TemplateSendMessage(alt_text='確認訊息', template=queries)

    line_bot_api.reply_message(reply_token, temp_msg)


#message = text = event.message.text

def ptt_check(event,reply_token):  #論壇熱門討論 - PTT / DCARD
    try:
        flex_message = [TextSendMessage(text='電影論壇即時熱度關鍵字'),
            ImageSendMessage(
            original_content_url = "https://i.imgur.com/8bCs9eH.png",
            preview_image_url = "https://i.imgur.com/8bCs9eH.png"
            ),
            TextSendMessage(text='要選擇哪個論壇的電影版呢?',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=URIAction(label="PTT", uri="https://www.ptt.cc/bbs/movie/index.html")),
                                    QuickReplyButton(action=URIAction(label="DCARD", uri="https://www.dcard.tw/f/movie"))
                                ]))
        ]
        line_bot_api.reply_message(reply_token, flex_message)
    except:
        line_bot_api.reply_message(reply_token,TextSendMessage(text='發生錯誤！'))



def personal(event,reply_token):  #論壇熱門討論 - PTT / DCARD
    try:
        flex_message = [
            TextSendMessage(text='要執行下列哪個動作呢?',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=URIAction(label="選擇個人電影喜好", uri="https://liff.line.me/1656658324-ydPdBBDr")),
                                    QuickReplyButton(action=PostbackAction(label="人臉特徵建模", data="action=open_camera"))
                                ]))
        ]
        line_bot_api.reply_message(reply_token, flex_message)
    except:
        line_bot_api.reply_message(reply_token,TextSendMessage(text='發生錯誤！'))




def manage_rating_Form(mtext,username):
#
    uname=username 
    mname=mtext.split('/')[0]
    rating=mtext.split('/')[1]
    print(f'{uname}{mname}{rating}')
    insert_ratingdata_to_mysql(uname,mname,rating)

#uname,like_movie_type,like_mname1,like_mname2,like_mname3
def manage_user_habit_Form(mtext,username):
    uname=username 
    like_movie_type=mtext.split('/')[0]
    like_mname1=mtext.split('/')[1]
    like_mname2=mtext.split('/')[2]
    like_mname3=mtext.split('/')[3]
    rating=mtext.split('/')[1]
    print(f'++++++++++{like_movie_type}{like_mname1}{like_mname3}')
    insert_user_habit(uname,like_movie_type,like_mname1,like_mname2,like_mname3)
        # message = TextSendMessage(
        #     text = text1
        # )
        #line_bot_api.reply_message(event.reply_token,message)
#
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def manage_booking_Form(mtext,username):
#
    uname=username 
    mname=mtext.split('/')[0]
    session=mtext.split('/')[1]
    print(f'______{uname}{mname}{session}')
    insert_bookingdata_to_mysql(uname,mname,session)



import os
if __name__ == "__main__":
    #sy_version
    app.run()

    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
