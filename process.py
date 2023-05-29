import openai
openai.api_key = ""
gpt_dict = {}

def textProcess(content,fromUser):
    if content[0]=='$':
        return mudae(content[1:],fromUser)
    elif content[0]=='!':
        return 'siuuuuu!'
    else:
        return gpt(content,fromUser)

def mudae(content,fromUser):
    return "Tokai Teio dayo!"

def gpt(content,fromUser):
    global gpt_dict
    messages = []
    if fromUser in gpt_dict:
        messages = gpt_dict[fromUser]
    if len(messages)>=20:
        return "Quota exceeded"
    messages.append({"role": "user", "content": content})
    print(len(messages))
    print("Current Messages:")
    for message in messages:
        print(message['role'],message['content'])
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    reply = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    gpt_dict[fromUser]=messages
    return reply


