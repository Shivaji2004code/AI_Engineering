import os
from dotenv import load_dotenv
from openai import OpenAI
from collections import defaultdict

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)
h = defaultdict(list)
system_prompt = """
You are given the website link You need to go to that website and just findout all the endpoints and all the 
links of the websites so that i scrape with it. Please ignore private pages but gather all the public and shared websites
You have to return with like this :
                                ['www.google.com',
                                www.gemni.google.com]
Make sure You only give the links in the output i will add to my hashmaps so that i can use it later donot give any
errors while giving output give the format exactly how i mentioned so that it will directly add to the hashmap.
it should contain all the links in an array and i wil directly append your op array in my dictionary.

"""
history = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_prompt = input("You : ")

    if user_prompt.lower() == "quit" or not user_prompt.strip():
        break

    history.append({
        "role": "user",
        "content": user_prompt
    })
    

    response = client.chat.completions.create(
        model="openai/gpt-4.1-nano",
        messages=history
    )

    reply = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": reply
    })

    h[user_prompt].append(reply)

    print("\nAI :", reply)
    print(h[0])

