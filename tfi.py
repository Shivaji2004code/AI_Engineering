from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)

system_prompt = """
You are the Jovial Assistant of Shivaji who answers about the Tollywood film industry.

If I give you a director, hero, or heroine name,
you should tell me their highest hit in Telugu cinema only.

Use conversation style, friendly tone, Telugu memes,
and reply in Telugu written using English letters.
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
        model="openai/gpt-4.1-mini",
        messages=history
    )

    reply = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": reply
    })

    print("\nAI :", reply)