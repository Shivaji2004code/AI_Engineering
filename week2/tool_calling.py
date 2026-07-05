from openai import OpenAI
import os
import gradio as gr
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("API_KEY")
)

history = [
    {
        'role' : 'system',
        'content' : 'You are a lazy assistant and you have to give the lazy answers if any tool is called inside you then you have to not perform anything and just return whats returned by the function as you are very lazy but just great if user greats you strictly you should return the fn value only no more improvisation'

    },
    {
        'role' : 'user',
        'content' : input('ASK :')
    }
]


def cars(car):
    car = car.lower()
    hash_map ={
        'toyota' : 'japan',
        'tata': 'india',
        'mahindra' : 'india',
        'honda' : 'japan',
        'byd' : 'china',
        'tesla' : 'america',
        'audi' : 'germany',
        'bmw' : 'germany',
        'maruthi' : 'india'

    }
    return hash_map.get(car, 'I dont know')

functions = {
    'cars' : cars
}

tools = [
    {
        'type' : 'function',
        'function': {
            'name' : 'cars',
            'description' : 'the cars from diff countries',
            'parameters' :{
                'type' : 'object', 
                'properties' : { 
                    'car' :{
                        'type' : 'string',
                        'description' : 'car company'

                    },
            
                },
                'required' : ['car']
        }
    }
    } 
]
response = client.chat.completions.create(
    model = 'openai/gpt-4.1-mini',
    messages = history,
    tools = tools
)

message = response.choices[0].message

if message.tool_calls:
    history.append(message)
    for tool_call in message.tool_calls:
        arguments = json.loads(tool_call.function.arguments)
        function_name = functions[tool_call.function.name]
        result = function_name(**arguments)

        history.append(
        {
            'role' : 'tool',
            'tool_call_id' : tool_call.id,
            'content' : result,
        }
    )
    
    final = client.chat.completions.create(
        model = 'openai/gpt-4.1-mini',
        messages = history,
        tools = tools,

    )
    message = final.choices[0].message

    print(final.choices[0].message.content)

    print(f"result :{result}")

else:
    print(message.content)
