import time
import requests
import json

url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send'
class LateMsg(object):
    def __init__(self):
        pass

    def send(self):
        return "success"

class LateTextMsg(LateMsg):
    def __init__(self, toUserName, content):
        self.data = {
            "touser": toUserName,
            "msgtype": "text",
            "text":{
                "content": content
            }
        }

    def send(self, access_token):
        params = {'access_token': access_token}
        headers = {'Content-Type': 'application/json'}
        json_payload = json.dumps(self.data)
        response = requests.post(url, params=params, headers=headers, data=json_payload)
        print(json_payload)
        if response.status_code == 200:
            print('Late reply successful')
        else:
            print('Request failed with status code:', response.status_code)


class LateImageMsg(LateMsg):
    def __init__(self, toUserName, media_id):
        self.data = {
            "touser":toUserName,
            "msgtype":"image",
            "image":{
              "media_id":media_id
            }
        }

    def send(self, access_token):
        params = {'access_token': access_token}
        headers = {'Content-Type': 'application/json'}
        json_payload = json.dumps(self.data)
        response = requests.post(url, params=params, headers=headers, data=json_payload)
        if response.status_code == 200:
            print('Late reply successful')
        else:
            print('Request failed with status code:', response.status_code)