import os
from dotenv import load_dotenv
import openai

load_dotenv(dotenv_path="c:/Users/vurja/Social Agent/Linky/linkedin_agent/.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_post(topic: str):
    prompt = f"Write a short, engaging LinkedIn post about {topic}."
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120
    )
    return response.choices[0].message.content.strip()
