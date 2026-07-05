from openai import OpenAI
from dotenv import load_dotenv
import os
import gradio as gr

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)

def ai(input_text):

    system_prompt = "You are a jovial assistant that is very good at explaining things in a simple way. "
    history =[
        {
            'role' : 'system',
            'content' : system_prompt
            }
    ]
    history.append(
        {
            'role' : 'user',
            'content' : input_text
        }
    )
    response = client.chat.completions.create(model='openai/gpt-4.1-mini',messages=history, stream=True
    )
    reply = """"""
    for chunk in response:
        asd = chunk.choices[0].delta.content
        if asd:
            reply += asd
    print(reply)
    yield reply



app = gr.Interface(fn = ai, inputs = gr.Textbox(label = "Enter your question"),outputs = gr.Markdown(label = "Answer"))

app.launch()



