import os
import random
from google import genai
from google.genai import types

class GenerativeAI:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.system_prompt = """You are a Sustainability Advisor AI. Your role is to:
        - Provide accurate information about SDGs and sustainable practices
        - Offer practical business sustainability recommendations
        - Explain complex environmental concepts in simple terms
        - Combine technical knowledge with practical implementation advice
        - Stay professional yet approachable in tone
        - Cite reliable sources when possible"""

    def generate_response(self, user_input, conversation_history):
        messages = [
            {"role": "system", "content": self.system_prompt},
            *conversation_history[-4:],  # Keep last 4 exchanges
            {"role": "user", "content": user_input}
        ]
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[user_input],
                config=types.GenerateContentConfig(
                    max_output_tokens=500,
                    temperature=0.1
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"AI Service Error: {str(e)}"

    def should_use_generative_ai(self, intent, tokens):
        if intent == 'unknown':
            return True
        if random.random() < 0.3 and intent in ['sustainability_query', 'sdg_info']:
            return True
        return False