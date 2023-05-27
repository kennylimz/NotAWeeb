import hashlib
from flask import Flask, request
import receive
import reply

app = Flask(__name__)

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
        print("Handle Post webdata is ", webData)
        # 后台打日志
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = recMsg.Content
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            print("暂且不处理")
            return "success"
    except Exception as Argment:
        return str(Argment)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)