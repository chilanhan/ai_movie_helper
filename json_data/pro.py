import os.path
import tempfile
import pymysql



from flask import Flask
app = Flask(__name__)

from flask import request, abort,render_template
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction, ImagemapArea, TemplateSendMessage, ButtonsTemplate, DatetimePickerTemplateAction
from urllib.parse import parse_qsl
import datetime
from linebot.models import (
    MessageEvent,QuickReplyButton,QuickReply,CarouselColumn,CarouselTemplate,CarouselContainer,MessageTemplateAction,URITemplateAction,PostbackTemplateAction,VideoMessage,TextMessage, StickerMessage, StickerSendMessage, ConfirmTemplate, TemplateSendMessage, MessageAction, URIAction, LocationMessage
 )

# from get_ten_pics_and_features import get_ten_pics_and_features
# from yahoodata_cv2_to_mysql import yahoo_mysql_to_carousel,yahoo_csv_to_mysql
# from mysql_insert import insert_user_to_mysql


yc_token='6LtqwU4k493Gys589ikza9GzxWgrHjJFIcDGc21+JcMAALUjLd2xLzGRJft575QbIOeaUEedDr6QMf4mormSu0bCA8QuUTGj0kC0Im1qNsovhsMLv8tHwJjE2PkLvA44E8ckPuLRtWlTu3sNq+rNmwdB04t89/1O/w1cDnyilFU='
yc_secret='62fedcb34c8415668774fd2ccdb5d73c'

sy_token='2IT+lGbqil5lJCuY8ijAtLswcNi3sShNWPLoBOxNzo3iwm5Ob+8JyNsymS9WQCsKYp7YEhtTAIC2+C2Dm2sMvztIsDoKAaYXDUKxfh6OkpqmObF0eK2+ebunvj4IWw/OiS0eac9a6eJXp1c+y7b3wAdB04t89/1O/w1cDnyilFU='
sy_secret='d91f9849821716b3500eb7686daf3f8b'

booking_liffid='1656658324-yQ56DDov'
rating_liffid='1656658324-7ddvPPk0'


line_bot_api = LineBotApi(sy_token)
handler = WebhookHandler(sy_secret)

#下載document
from flask import send_from_directory
import flask
@app.route('/downloads_json')

def download():
    filename = "user_face_info.json"
    dirpath=app.root_path

    return send_from_directory(dirpath,filename,as_attachment=True)


@app.route('/booking_page')
def booking_page():
    return render_template('booking_page.html', liffid = booking_liffid)

@app.route('/rating_page')
def rating_page():
    return render_template('rating_page.html', liffid = rating_liffid)



@app.route("/callback", methods=['POST'])

def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    userid = event.source.user_id
    profile = line_bot_api.get_profile(str(userid))
    username=profile.display_name
    print(userid,username)

    insert_user_to_mysql(userid,username)


    if mtext == '@圖片地圖':
        sendImgmap(event)

    elif mtext == '@日期時間':
        sendDatetime(event)

    elif mtext == '@儲存人臉特徵':
        user_camera_open(event)

    elif mtext == '@看電影評論':
        comment_show(event)

    elif mtext =='@其他功能':
        line_bot_api.reply_message(event.reply_token,TextSendMessage('@台灣電影票房排行'))
    elif mtext == '@id':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(userid))

    elif mtext == '@name':
        try:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(username))
        except LineBotApiError as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('no name'))
    elif mtext == '1':
        sendCarousel(event)

    elif mtext[:3] == '###' and len(mtext) > 3:
        manageForm(event, mtext)







def sendCarousel(event):  #轉盤樣板
    yahoo_csv_to_mysql()
    result=yahoo_mysql_to_carousel()
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=result[0][6],
                        title=result[0][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[0][0],result[0][3],result[0][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[0][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[0][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[1][6],
                        title=result[1][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[1][0], result[1][3], result[1][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[1][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[1][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[2][6],
                        title=result[2][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[2][0], result[2][3], result[2][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[2][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[2][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[3][6],
                        title=result[3][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[3][0], result[3][3], result[3][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[3][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[3][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[4][6],
                        title=result[4][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[4][0], result[4][3], result[4][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[4][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[4][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[5][6],
                        title=result[5][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[5][0], result[5][3], result[5][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[5][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[5][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[6][6],
                        title=result[6][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[6][0], result[6][3], result[6][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[6][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[6][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[7][6],
                        title=result[7][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[7][0], result[7][3], result[7][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[7][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[7][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[8][6],
                        title=result[8][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[8][0], result[8][3], result[8][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[8][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[8][4]

                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=result[9][6],
                        title=result[9][1],
                        text='第{}名\n上映時間：{}\n網友評分：{}'.format(result[9][0], result[9][3], result[9][5]),
                        actions=[

                            URITemplateAction(
                                label='電影介紹',
                                uri=result[9][2]

                            ),
                            URITemplateAction(
                                label='電影預告',
                                uri=result[9][4]

                            ),

                        ]
                    ),





                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



#儲存影片
@handler.add(MessageEvent,message=(VideoMessage))
def handle_content_message(event):
    userid = event.source.user_id
    profile = line_bot_api.get_profile(str(userid))
    username = profile.display_name
    static_tmp_path='./resources'


    message_content=line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path,prefix=username+'___',delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path=tf.name

    dist_path=tempfile_path+'.mp4'
    dist_name=os.path.basename(dist_path)
    os.rename(tempfile_path,dist_path)

    print('./resources/'+dist_name)

    get_ten_pics_and_features('./resources/'+dist_name,username)


    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='成功搜集人臉特徵'),
            TextSendMessage(text=dist_name),

        ]


    )



@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件

def comment_show(event):
    flex_message = TextSendMessage(text='以下有雷，請小心',
                                   quick_reply=QuickReply(items=[
                                       QuickReplyButton(action=MessageAction(label="PTT",
                                                                             text="https://www.ptt.cc/bbs/movie/index.html")),
                                       QuickReplyButton(action=MessageAction(label="DCARD",
                                                                             text="https://www.dcard.tw/f/movie")),

                                   ]))
    line_bot_api.reply_message(event.reply_token, flex_message)



def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  #取得data資料
    if backdata.get('action') == 'sell':
        sendData_sell(event, backdata)


def user_camera_open(event):
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

    line_bot_api.reply_message(event.reply_token, temp_msg)





def sendImgmap(event):  #圖片地圖
    try:
        image_url = 'https://i.imgur.com/Yz2yzve.jpg'  #圖片位址
        imgwidth = 1040  #原始圖片寛度一定要1040
        imgheight = 300
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text="圖片地圖範例",
            base_size=BaseSize(height=imgheight, width=imgwidth),  #圖片寬及高
            actions=[
                MessageImagemapAction(  #顯示文字訊息
                    text='你點選了紅色區塊！',
                    area=ImagemapArea(  #設定圖片範圍:左方1/4區域
                        x=0,
                        y=0,
                        width=imgwidth*0.25,
                        height=imgheight
                    )
                ),
                URIImagemapAction(  #開啟網頁
                    link_uri='http://www.e-happy.com.tw',
                    area=ImagemapArea(  #右方1/4區域(藍色1)
                        x=imgwidth*0.75,
                        y=0,
                        width=imgwidth*0.25,
                        height=imgheight
                    )
                ),
            ]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendDatetime(event):  #日期時間
    try:
        message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間示範',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell&mode=date",  #觸發postback事件
                        mode="date",  #選取日期
                        initial="2020-10-01",  #顯示初始日期
                        min="2020-10-01",  #最小日期
                        max="2021-12-31"  #最大日期
                    ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="action=sell&mode=time",
                        mode="time",  #選取時間
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                    ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="action=sell&mode=datetime",
                        mode="datetime",  #選取日期時間
                        initial="2020-10-01T10:00",
                        min="2020-10-01T00:00",
                        max="2021-12-31T23:59"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendData_sell(event, backdata):  #Postback,顯示日期時間
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')  #讀取日期
        elif backdata.get('mode') == 'time':
            dt = '時間為：' + event.postback.params.get('time')  #讀取時間
        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')  #讀取日期時間
            dt = dt.strftime('{d}%Y-%m-%d, {t}%H:%M').format(d='日期為：', t='時間為：')  #轉為字串
        message = TextSendMessage(
            text=dt
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def manageForm(event, mtext):
    try:
        flist = mtext[3:].split('/')
        text1 = '姓名：' + flist[0] + '\n'
        text1 += '日期：' + flist[1] + '\n'
        text1 += '包廂：' + flist[2]
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


import os
if __name__ == "__main__":
    #sy_version
    app.run()