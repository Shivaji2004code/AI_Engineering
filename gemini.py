from openai import OpenAI
from key import openrouter_key

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = openrouter_key
)

history = [{
    'role' : 'system',
    'content' : """
    You are the Geography expert assistant who helps users saying the capital city of the country mentioned by the user
    1. user prompts with the country name you have just reply with the capital city of that country
    2. If the user asks about previous countries/capitals discussed, look back at the conversation history and list them.
    3. Greet the people well in the first message if they greet you with Hi or Hello
    4. Do not give the answers for refusal please them and sorry for not giving that type of answers if not related to your subject
    
    """
    
}]
while True:
    user_input = input('Enter the Input: ')
    if user_input == 'quit' or not user_input:
        break


    history.append({'role' : 'user', 'content' : user_input})
    response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=history,
        )
    reply = response.choices[0].message.content

    history.append({'role':'assistant', 'content' : reply})
    print('AI : ', reply)