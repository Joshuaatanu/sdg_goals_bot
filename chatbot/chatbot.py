import openai
from dotenv import load_dotenv
import os
from .nlp import NLPProcessor
from .sdg import SDGManager
from .generative_ai import GenerativeAI

class AISustainabilityChatbot:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        self.nlp_processor = NLPProcessor()
        self.sdg_manager = SDGManager()
        self.generative_ai = GenerativeAI()
        self.conversation_history = []

    def generate_response(self, user_input):
        tokens = self.nlp_processor.preprocess_text(user_input)
        intent = self.nlp_processor.get_intent(tokens)
        
        self.conversation_history.append({"role": "user", "content": user_input})
        
        if self.generative_ai.should_use_generative_ai(intent, tokens):
            ai_response = self.generative_ai.generate_response(user_input, self.conversation_history)
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return self.nlp_processor.postprocess_ai_response(ai_response)
        
        if intent == 'sdg_info':
            sdg_number = self.nlp_processor.extract_sdg_number(user_input)
            response = self.sdg_manager.get_sdg_info(sdg_number)
        else:
            response = self.nlp_processor.get_response(intent)
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def start_chat(self):
        print("Chatbot: Welcome to the Sustainability Advisor! Type 'exit' to end.")
        while True:
            user_input = input("\nUser: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Chatbot: Thank you for your commitment to sustainability!")
                break
            response = self.generate_response(user_input)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    bot = AISustainabilityChatbot()
    bot.start_chat() 