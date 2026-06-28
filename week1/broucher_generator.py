import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_KEY")
)

while True:
    user_prompt = input("You : ")

    if user_prompt.lower() == "quit" or not user_prompt.strip():
        break
    
    def endpoint_parsing(user_prompt):
        system_prompt = """
                You are a web crawler assistant. You will be given a website URL.

                Your task is to analyze the website and extract ALL publicly accessible URLs and endpoints, including:
                - Navigation links
                - Subdomains
                - API endpoints (if publicly visible)
                - Linked pages

                Rules:
                - IGNORE private, authentication-required, or admin pages
                - ONLY return publicly accessible URLs
                - Return ONLY valid JSON — no explanation, no comments, no markdown, no extra text
                - Every URL must be a properly formatted string
                - Do not include duplicate URLs

                Output format (strictly follow this):
                {
                "urls": [
                    "https://www.example.com",
                    "https://blog.example.com",
                    "https://www.example.com/about"
                ]
                }

                Any deviation from this format will break the pipeline. Return the JSON object and nothing else.

                """
        history = [
                {"role": "system", "content": system_prompt},
                {'role' : 'user', 'content' : user_prompt}
        ]


        response = client.chat.completions.create(
            model="openai/gpt-4.1-nano",
            messages=history
        )

        reply = response.choices[0].message.content

        
        return reply

    def matter_parsing(data):
        system_prompt = """
        You are a web content parser agent. You will receive a JSON object containing 
                a list of website URLs and endpoints as your input.

                Your task is to visit each URL, extract ONLY the meaningful text content 
                present on that page, including:
                - Main body text and paragraphs
                - Headings and subheadings
                - Product or service descriptions
                - About us, mission, vision statements
                - Contact details (email, phone, address)
                - Any other readable business-relevant text

                Rules:
                - Extract ONLY plain readable text — NO HTML tags, NO CSS, NO JavaScript
                - Do NOT include tag names, attributes, or any code
                - Do NOT summarize or modify the content — return it as-is
                - Do NOT add explanations, comments, or markdown
                - If a URL is unreachable or returns an error, set its value to null
                - Return ONLY a valid JSON object — nothing else

                Input format you will receive:
                {
                "urls": [
                    "https://www.example.com",
                    "https://www.example.com/about",
                    "https://www.example.com/services"
                ]
                }

                Output format (strictly follow this):
                {
                "parsed_data": {
                    "https://www.example.com": {
                    "title": "Example Company",
                    "content": "Welcome to Example Company. We provide world-class solutions..."
                    },
                    "https://www.example.com/about": {
                    "title": "About Us",
                    "content": "Founded in 2010, Example Company has been a leader in..."
                    },
                    "https://www.example.com/services": {
                    "title": "Our Services",
                    "content": "We offer a range of services including consulting, development..."
                    }
                }
                }

                Any deviation from this format will break the pipeline. 
                Return the JSON object and nothing else.
                        
        
        """
        history = [{
            'role' : 'system',
            'content' : system_prompt
        },
        {
            'role' : 'user',
            'content' : data
        }
        ]


        response = client.chat.completions.create(
            model="openai/gpt-5-nano",
            messages=history

        )

        result = response.choices[0].message.content

        return result

    def broucher_data(matter):
        system_prompt = """
        You are an expert brochure designer and copywriter working for a world-class 
        creative agency. You have designed brochures for Fortune 500 companies, 
        top-tier startups, and global brands. Your work is known for being polished, 
        professional, and compelling.

        You will receive a JSON object containing URLs and their parsed text content 
        from a company's website as your input.

        Your task is to read and understand all the content provided, then craft a 
        stunning, professional company brochure written in Markdown format.

        The brochure must include the following sections (use only what is relevant 
        from the data, skip sections if data is insufficient):

        1. Cover — Company name, tagline, and a one-line powerful brand statement
        2. About Us — Who the company is, their story, mission, and vision
        3. What We Do — Core services or products, described clearly and compellingly
        4. Why Choose Us — Unique value propositions, strengths, differentiators
        5. Our Impact — Stats, achievements, milestones, or client results if available
        6. Our Team — Key people or leadership if mentioned
        7. Contact Us — Address, phone, email, website, social links if available
        8. Call to Action — A strong closing statement that drives engagement

        Writing Rules:
        - Write in a confident, professional, and engaging tone
        - Do NOT copy-paste raw content — rewrite it to sound polished and premium
        - Use powerful, action-driven language throughout
        - Keep each section concise but impactful — quality over quantity
        - Do NOT mention URLs, endpoints, or any technical terms in the brochure
        - Do NOT add any explanation outside the markdown brochure
        - Return ONLY the markdown content — nothing else

        Markdown Design Rules:
        - Use # for the company name on the cover
        - Use ## for major section headings
        - Use ### for subheadings within sections
        - Use > for powerful quotes, taglines, or mission statements
        - Use --- to separate major sections
        - Use **bold** for key terms, names, and highlights
        - Use bullet points for lists of services, features, or achievements
        - Make it visually structured so it renders beautifully

        Input format you will receive:
        {
        "parsed_data": {
            "https://www.example.com": {
            "title": "Example Company",
            "content": "Welcome to Example Company. We provide world-class solutions..."
            },
            "https://www.example.com/about": {
            "title": "About Us",
            "content": "Founded in 2010, Example Company has been a leader in..."
            },
            "https://www.example.com/services": {
            "title": "Our Services",
            "content": "We offer consulting, development, and design services..."
            }
        }
        }

        Return ONLY the markdown brochure. No explanations, no comments, no JSON. 
        Just the beautifully written and structured markdown file, ready to export.
        
        
        """


        history = [{
            "role" : "system",
            "content" : system_prompt
        },
        {
            'role' : 'user',
            'content' : matter
        }]

        response = client.chat.completions.create(
            model = "openai/gpt-4.1-mini",
            messages = history,
            stream = True
        )

        for chunk in response:
            reply = chunk.choices[0].delta.content
            if reply is not None:
                print(reply, end='', flush=True)


    data = endpoint_parsing(user_prompt)
    matter = matter_parsing(data)
    broucher_data(matter)




