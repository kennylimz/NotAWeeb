import openai
import time
openai.api_key = "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"
gpt_dict = {}

def textProcess(content,fromUser,duplicated=False):
    if content[0]=='$':
        return mudae(content[1:],fromUser)
    elif content[0]=='!':
        return "siuuuuu!"
    else:
        return gpt(content,fromUser,duplicated)

def mudae(content,fromUser):
    return "Tokai Teio dayo!"

def gpt(content,fromUser,getLast=False):
    global gpt_dict
    time0 = time.time()
    messages = []
    if fromUser in gpt_dict:
        messages = gpt_dict[fromUser]
    if len(messages)>=20:
        return "Quota Exceeded"
    elif getLast:
        print("Trying to rechieve last reply...")
        if messages[-1]["role"]=="assistant":
            return messages[-1]['content']
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


