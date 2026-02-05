import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. Point the client to Groq's server
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

class LLMNode:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    # 2. Use a free model (Llama-3) instead of GPT-4
    def generate(self, user_prompt, model="llama-3.3-70b-versatile", json_mode=False):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        kwargs = {"model": model, "messages": messages}
        
        # Groq supports JSON mode slightly differently, but this usually works.
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
            
        try:
            response = client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            return json.loads(content) if json_mode else content
        except Exception as e:
            return {"error": str(e)}