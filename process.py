import openai
import time
import mudae
from threading import Thread
import lateReply

openai.api_key = ""
gpt_dict = {}

def textProcess(content,fromUser,duplicated=False,access_token=None):
    if content[0]=='$':
        return mudaeReply(content[1:],fromUser),"image"
    elif content[0]=='!':
        return "siuuuuu!","text"
    else:
        thread = Thread(target=gpt, args=(content,fromUser,duplicated,access_token))
        thread.start()
        return "success","gpt"

def mudaeReply(content,fromUser):
    return mudae.processMudae(content,fromUser)

def gpt(content,fromUser,getLast=False,access_token=None):
    global gpt_dict
    time0 = time.time()
    messages = []
    if fromUser in gpt_dict:
        messages = gpt_dict[fromUser]
    if len(messages)>=30:
        lateMsg = lateReply.LateTextMsg(fromUser, "（请求超过限额）")
        lateMsg.send(access_token)
    elif getLast:
        print("Trying to rechieve last reply...")
        if messages[-1]["role"]=="assistant":
            lateMsg = lateReply.LateTextMsg(fromUser,messages[-1]['content'])
            lateMsg.send(access_token)
        else:
            lateMsg = lateReply.LateTextMsg(fromUser,"（请求过多）")
            lateMsg.send(access_token)
    else:
        messages.append({"role": "user", "content": content})
        print(len(messages))
        print("Current Messages:")
        for message in messages:
            print(message['role'],message['content'])
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        reply = chat_completion.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        gpt_dict[fromUser]=messages
        print("Generate Time:", time.time()-time0)
        lateMsg = lateReply.LateTextMsg(fromUser,reply)
        lateMsg.send(access_token)



