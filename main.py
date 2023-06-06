import hashlib
import time

import requests
from flask import Flask, request
import receive
import reply
import process
from flask_apscheduler import APScheduler
import pymysql
import mudae

class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
msgIds = []
# response = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx89ada809e95adb96&secret=")
# access_token = response.json()['access_token']
connection = pymysql.connect(
    host='34.31.231.212',
    port= 3306,
    user='root',
    password='12345678'
)

@scheduler.task('cron', id='clear_quota', minute='0')
def job1():
    process.gpt_dict.clear()
    mudae.reset(connection)
    print("Quota Cleared")

@scheduler.task('interval', id='reset_connection', minutes=15)
def job2():
    global connection
    connection.commit()
    connection.close()
    connection = pymysql.connect(
        host='34.31.231.212',
        port=3306,
        user='root',
        password='12345678'
    )
    print("Connection Reset")


# @scheduler.task('interval', id='get_token', minutes=60)
# def job2():
#     global  access_token
#     response = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx89ada809e95adb96&secret=afaa7edfa9f8d54cc8b68c48be4aef19")
#     access_token = response.json()['access_token']
#     print("access_token refreshed")
#

@app.route('/wx', methods=['GET'])
def handleGet():
    try:
        data = request.args
        if len(data) == 0:
            return "hello, this is handle view"
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        token = "WECHAT"
        string_list = [token, timestamp, nonce]
        string_list.sort()
        sha1 = hashlib.sha1()
        for item in string_list:
            sha1.update(item.encode('utf-8'))
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature:", hashcode, signature)
        if hashcode == signature:
            return echostr
        else:
            return ""
    except Exception as Argument:
        return str(Argument)


@app.route('/wx', methods=['POST'])
def handlePost():
    try:
        webData = request.data.decode('utf-8')
        print("Handle Post webdata is:\n", webData)
        # 后台打日志
        recMsg = receive.parse_xml(webData)
        duplicated = False
        if recMsg.MsgId in msgIds:
            duplicated = True
        else:
            msgIds.append(recMsg.MsgId)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            recContent = recMsg.Content.decode('utf-8')
            if recContent[0] == '$' and len(recContent)>1:
                replyContent, replyType = mudae.processMudae(recContent[1:],toUser,connection)
            else:
                replyContent, replyType = process.textProcess(recContent, toUser, duplicated)
            # if replyType == "gpt":
            #     return "success"
            if replyType == "text":
                replyMsg = reply.TextMsg(toUser, fromUser, replyContent)
            elif replyType == "image":
                replyMsg = reply.ImageMsg(toUser, fromUser, replyContent)
            print("Reply:", replyContent)
            return replyMsg.send()
        else:
            return "success"
    except Exception as Argment:
        return str(Argment)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
