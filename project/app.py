from flask import Flask,render_template, request
import os
import requests as rq
from pprint import pprint as pp
import random

app=Flask(__name__)

token=os.getenv("TELEGRAM_TOKEN")
base_url="https://api.hphk.io/telegram"
my_url="https://webhook-onelifefirebat.c9users.io" #webhook으로 오는 데이터의 라우터 url은 비번(토큰 등)으로!
naver_id=os.getenv("NAVER_CLOVA_ID")
naver_secret=os.getenv("NAVER_CLOVA_SECRET")


########################################################################
def sendMessage(token,chat_id,text):
    send_url=base_url+"/bot{}/sendMessage?chat_id={}&text={}".format(token,chat_id,text)
    rq.get(send_url)

@app.route("/")
def index():
    return render_template("index.html")

### Webhook
# 웹훅 설정 (set webhook)==Let the telegram role a noticer. (telegram method setWebhook?url=)
@app.route("/setwebhook")
def setwebhook():
    url=base_url+"/bot{}/setWebhook?url={}/{}".format(token,my_url,token) #url for webhook
    res=rq.get(url)
    print(res)
    return "{}".format(res),200 # message, 200
    
# 웹훅을 통해 정보가 들어올 route, 보안적으로 텔레그렘과 나만 알기 위해!
@app.route("/{}".format(token),methods=["POST"]) ### 웹훅을 통해 post방식으로 보냄.
def telegram():
    doc=request.get_json() #그냥 바로 받넹. flask request가.
    pp(doc)
    chat_id=doc["message"]["chat"]["id"]
    text=doc["message"].get("text") ## get을 쓰면 없는 키에 접근하면 None 리턴
    
    
    # if msg=="로또":
    #     msg=sorted(random.sample(list(range(1,46)),6))
        
    # sendMessage(token,chat_id,msg)
    # # No matter what message come in, just respond as "Shut up"
    # return "", 200
# 200status 코드로 응답을 해주어야 함.
    
    img = False
    
    if doc.get('message').get('photo') is not None:
        img = True
    
    if img:
        file_id = doc.get('message').get('photo')[-1].get('file_id')
        file = rq.get("{}/bot{}/getFile?file_id={}".format(base_url, token, file_id))
        file_url = "{}/file/bot{}/{}".format(base_url, token, file.json().get('result').get('file_path'))
        
        # 네이버로 요청
        res = rq.get(file_url, stream=True)
        clova_res = rq.post('https://openapi.naver.com/v1/vision/celebrity',
            headers={
                'X-Naver-Client-Id':naver_id,
                'X-Naver-Client-Secret':naver_secret
            },
            files={
                'image':res.raw.read()
            })
        if clova_res.json().get('info').get('faceCount'):
            print(clova_res.json().get('faces'))
            text = "{}".format(clova_res.json().get('faces')[0].get('celebrity').get('value'))
        else:
            text = "인식된 사람이 없습니다."
    else:
    	# text 처리
    	text = doc['message']['text']
        
    rq.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(base_url, token, chat_id, text))
    return '', 200
    
    
    

# telegram -> give a notice to this server. if specific users send message to the chatbot
# telegram will send something in the form of json
@app.route('/delete_webhook')
def delete_webhook():
    res = rq.get('https://api.hphk.io/telegram/bot{1}/deleteWebhook?url={2}/{3}'.format(token, my_url, token))
    print(res.text)
    return '{}'.format(res), 200
    
    



