from flask import Flask, request
import receive
import reply

app = Flask(__name__)

@app.route('/wx', methods=['GET'])
def handleGet():
    return "hello, this is get handle view"

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
            content = "test"
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            print("暂且不处理")
            return "success"
    except Exception as Argment:
        return str(Argment)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)