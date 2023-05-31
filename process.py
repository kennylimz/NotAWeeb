import openai
import time
import mudae
openai.api_key = ""
gpt_dict = {}

def textProcess(content,fromUser,duplicated=False):
    if content[0]=='$':
        return mudaeReply(content[1:],fromUser),"image"
    elif content[0]=='!':
        return "siuuuuu!","text"
    else:
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
        return "Quota Exceeded"
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


