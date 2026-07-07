from openai import OpenAI
from dotenv import load_dotenv
import os
import gradio as gr
from products_data import products
import json


load_dotenv()

cart = []
prompt = True
while prompt:
    user_prompt = input('ASK : ')
    if user_prompt.lower() == 'quit':
        break
    history = [{
        "role": "system",
        "content": "You are a helpful shopping assistant. You can search for products, check prices, check stock availability, add products to the cart, and remove products from the cart."
    },
    {
        "role": "user",
        "content": user_prompt
    }
    ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("API_KEY")
    )
    def search_product(name):
        if name in products and products[name]["stock"] > 0:
            return f"Yes, {name} is available."
        return 'Sorry, we do not have that product in stock.'

    def get_price(name):
        if name in products:
            return f'The price of {name} is ${products[name]["price"]}.'
        return 'Sorry, we do not have that product in stock.'

    def check_stock(name):
        if name in products:
            stock = products[name]["stock"]
            if stock > 0:
                return f'The product {name} is in stock. Quantity available: {stock}.'
            else:
                return f'Sorry, the product {name} is currently out of stock.'
        return 'Sorry, we do not have that product in stock.'

    def add_to_cart(name):
        if name in products:
            stock = products[name]["stock"]
            if stock > 0:
                cart.append(name.lower())
                products[name]["stock"] -= 1
                return f'{name} has been added to your cart.'
            else:
                return f'Sorry, the product {name} is currently out of stock.'
        return 'Sorry, we do not have that product in stock.'

    def remove_from_cart(name):
        if name in cart:
            cart.remove(name)
            products[name]["stock"] += 1
            return f'{name} has been removed from your cart.'
        return 'Sorry, that product is not in your cart.'

    def show_cart():
        if cart:
            return f'Your cart contains: {", ".join(cart)}.'
        return 'Your cart is empty.'


    functions = {
        'search_product': search_product,
        'get_price': get_price,
        'check_stock': check_stock,
        'add_to_cart': add_to_cart,
        'remove_from_cart': remove_from_cart,
        'show_cart': show_cart

    }

    tools = [
        {
            'type' : 'function',
            'function' : {
                'name' : 'search_product',
                'description' : 'Search for a product by name.',
                'parameters' : {
                    'type' : 'object',
                    'properties' : {
                        'name' : {
                            'type' : 'string',
                            'description' : 'The name of the product to search for.'
                        }
                    },
                    'required' : ['name']
                }
            }
    },
    {
        'type' : 'function',
        'function' : {
            'name' : 'get_price',
            'description' : 'Get the price of a product by name.',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'name' : {
                        'type' : 'string',
                        'description' : 'The name of the product to get the price for.'
                    }
                },
                'required' : ['name']
            }
        }
    },
    {
        'type' : 'function',

        'function' : {
            'name' : 'check_stock',
            'description' : 'Check the stock availability of a product by name.',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'name' : {
                        'type' : 'string',
                        'description' : 'The name of the product to check stock for.'
                    }
                },
                'required' : ['name']
            }
        },
    },
    {
        'type' : 'function',
        'function' : {
            'name' : 'add_to_cart',
            'description' : 'Add a product to the shopping cart by name.',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'name' : {
                        'type' : 'string',
                        'description' : 'The name of the product to add to the cart.'
                    }
                },
                'required' : ['name']
            }
        },
    },
    {
        'type' : 'function',
        'function' : {
            'name' : 'remove_from_cart',
            'description' : 'Remove a product from the shopping cart by name.',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'name' : {
                        'type' : 'string',
                        'description' : 'The name of the product to remove from the cart.'
                    }
                },
                'required' : ['name']
    }
    }
    },
    {
        'type' : 'function',
        'function' : {
            'name' : 'show_cart',
            'description' : 'Show the contents of the shopping cart.',
            'parameters' : {
                'type' : 'object',
                'properties' : {}
            }
        }
    }
    ]


    response = client.chat.completions.create(
        model='openai/gpt-4.1-mini',
        messages=history,
        tools = tools
    )

    message = response.choices[0].message
    if message.tool_calls:
        history.append(message)
        for tool_call in message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            function_name = functions[tool_call.function.name]
            result = function_name(**arguments)

            history.append({
                'role': 'tool',
                'tool_call_id': tool_call.id,
                'content': result,
            })

        final = client.chat.completions.create(
            model='openai/gpt-4.1-mini',
            messages=history,
            tools=tools
        )
        final_reply = final.choices[0].message.content
        print(final.choices[0].message.content)

        


    
    else:
        print(message.content)









        










