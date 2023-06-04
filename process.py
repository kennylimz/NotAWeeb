import openai
import time
import mudae
from threading import Thread
import lateReply

openai.api_key = ""
gpt_dict = {}

def textProcess(content,fromUser,duplicated=False):
    if content[0]=='!':
        return "siuuuuu!","text"
    else:
        # thread = Thread(target=gpt, args=(content,fromUser,duplicated,access_token))
        # thread.start()
        return gpt(content,fromUser,duplicated),"text"

def mudaeReply(content,fromUser):
    return mudae.processMudae(content,fromUser)

def gpt(content,fromUser,getLast=False):
    global gpt_dict
    time0 = time.time()
    messages = []
    if fromUser in gpt_dict:
        messages = gpt_dict[fromUser]
    if len(messages)>=30:
        return "（请求超过限额）"
    elif getLast:
        print("Trying to rechieve last reply...")
        if messages[-1]["role"]=="assistant":
            return messages[-1]['content']
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
    return reply



