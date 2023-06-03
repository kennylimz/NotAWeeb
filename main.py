import hashlib
import time

from flask import Flask, request
import receive
import reply
import process
from flask_apscheduler import APScheduler


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
msgIds = []


@scheduler.task('interval', id='clear_quota', minutes=60)
def job1():
    process.gpt_dict.clear()
    print("Quota Cleared")


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
            replyContent, replyType = process.textProcess(recContent, toUser, duplicated, access_token="69_fyjhOJKffsk2g1Akf_RFH91JZc7Exf0RtYiu0s4wkqws88Utize9Y1x60QaomW2shKaXIf0g012kIqWoisOV8jDlsfOmolS6m_uEGgzp6EZVhHWN5zpwwpGb5QcWKNaABAESV")
            if replyType == "gpt":
                return "success"
            elif replyType == "text":
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
