import openai
openai.api_key = "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"
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
    if fromUser in gpt_dict:
        messages = gpt_dict[fromUser]
    else:
        messages = []
    if len(messages)>=10:
        return "Quota exceeded"
    messages.append({"role": "user", "content": content})
    print("Current Messages:")
    for message in messages:
        print(message['user'],message['content'])
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply


