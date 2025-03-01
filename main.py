import openai
from dotenv import load_dotenv
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import re

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Download required NLTK resources
nltk.download(['punkt', 'wordnet', 'stopwords'])

class AISustainabilityChatbot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.intents = {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'greetings'],
                'responses': [
                    "Hello! How can I assist with your sustainability queries today?",
                    "Hi there! Ready to explore sustainable business practices?"
                ]
            },
            'sustainability_query': {
                'patterns': ['sustainab', 'eco-friendly', 'green', 'environment', 'carbon', 'sdg'],
                'responses': [
                    "Here are key strategies for sustainable businesses: \n1. Energy efficiency improvements\n2. Waste reduction programs\n3. Sustainable supply chain management\n4. Renewable energy adoption",
                    "Businesses can align with SDGs by: \n- Conducting sustainability audits\n- Engaging stakeholders\n- Setting measurable goals\n- Reporting transparently"
                ]
            },
            'sdg_info': {
                'patterns': ['sdg \\d+', 'goal \\d+', 'sustainable development goal'],
                'responses': self._load_sdg_responses(),
                'extract_sdg': True
            },
            'help': {
                'patterns': ['help', 'support', 'assist'],
                'responses': [
                    "I can help with:\n- Sustainability strategy advice\n- SDG alignment guidance\n- Eco-friendly practice recommendations"
                ]
            },
            'farewell': {
                'patterns': ['bye', 'goodbye', 'exit', 'quit'],
                'responses': ["Goodbye! Remember: Sustainability is a journey, not a destination!"]
            }
        }
        
        # Generative AI configuration
        self.generative_config = {
            "temperature": 0.7,
            "max_tokens": 150,
            "top_p": 1.0,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.2,
        }
        
        self.system_prompt = """You are a Sustainability Advisor AI. Your role is to:
        - Provide accurate information about SDGs and sustainable practices
        - Offer practical business sustainability recommendations
        - Explain complex environmental concepts in simple terms
        - Combine technical knowledge with practical implementation advice
        - Stay professional yet approachable in tone
        - Cite reliable sources when possible"""
        
        self.conversation_history = []

    def _load_sdg_responses(self):
        """Load SDG information from a data structure"""
        return {
            1: "SDG 1: No Poverty - Promote inclusive economic policies and living wages.",
            2: "SDG 2: Zero Hunger - Support sustainable agriculture and reduce food waste.",
            3: "SDG 3: Good Health - Implement workplace wellness programs and safety measures.",
            4: "SDG 4: Quality Education - Provide employee training on sustainability practices.",
            5: "SDG 5: Gender Equality - Ensure equal pay and leadership opportunities.",
            6: "SDG 6: Clean Water - Reduce water consumption and prevent pollution.",
            7: "SDG 7: Affordable Energy - Transition to renewable energy sources.",
            8: "SDG 8: Decent Work - Maintain ethical labor practices throughout supply chains.",
            9: "SDG 9: Innovation - Invest in sustainable technologies and infrastructure.",
            10: "SDG 10: Reduced Inequality - Promote diversity and inclusion initiatives.",
            11: "SDG 11: Sustainable Cities - Optimize logistics and reduce urban pollution.",
            12: "SDG 12: Responsible Consumption - Implement recycling and circular economy models.",
            13: "SDG 13: Climate Action - Measure carbon footprint and set reduction targets.",
            14: "SDG 14: Life Below Water - Reduce plastic use and prevent ocean pollution.",
            15: "SDG 15: Life on Land - Source materials sustainably and protect ecosystems.",
            16: "SDG 16: Peace and Justice - Ensure ethical governance and anti-corruption measures.",
            17: "SDG 17: Partnerships - Collaborate with NGOs and government organizations."
        }

    def _preprocess_text(self, text):
        """Clean and normalize input text"""
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens
                  if token not in self.stop_words]
        return tokens

    def _get_intent(self, tokens):
        """Determine intent with confidence scoring"""
        matched_intent = None
        highest_confidence = 0

        for intent_name, intent_data in self.intents.items():
            score = 0
            for pattern in intent_data['patterns']:
                if re.search(pattern, ' '.join(tokens)):
                    score += 1
                score += sum(1 for token in tokens if token.startswith(pattern))
            
            if score > highest_confidence:
                highest_confidence = score
                matched_intent = intent_name

        return matched_intent if highest_confidence >= 1 else 'unknown'

    def _extract_sdg_number(self, text):
        """Extract SDG number from query"""
        match = re.search(r'sdg (\d{1,2})|goal (\d{1,2})', text)
        if match:
            return int(match.group(1) or match.group(2))
        return None

    def _generate_ai_response(self, user_input):
        """Use OpenAI API for generative responses"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history[-4:],  # Keep last 2 exchanges
            {"role": "user", "content": user_input}
        ]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                **self.generative_config
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"AI Service Error: {str(e)}"

    def _should_use_generative_ai(self, intent, tokens):
        """Determine when to use generative AI"""
        if intent == 'unknown':
            return True
        if random.random() < 0.3 and intent in ['sustainability_query', 'sdg_info']:
            return True
        return False

    def _postprocess_ai_response(self, response):
        """Ensure AI responses align with our scope"""
        prohibited_terms = ["sorry", "apologize", "as an AI"]
        if any(term in response.lower() for term in prohibited_terms):
            return "I recommend focusing on sustainable business practices. Could you clarify your question?"
        return f"{response}\n\n[AI-generated suggestion - verify with official sources]"

    def generate_response(self, user_input):
        """Hybrid response generation system"""
        tokens = self._preprocess_text(user_input)
        intent = self._get_intent(tokens)
        
        self.conversation_history.append({"role": "user", "content": user_input})
        
        if self._should_use_generative_ai(intent, tokens):
            ai_response = self._generate_ai_response(user_input)
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return self._postprocess_ai_response(ai_response)
        
        if intent == 'sdg_info':
            sdg_number = self._extract_sdg_number(user_input)
            if sdg_number in self.intents['sdg_info']['responses']:
                response = self.intents['sdg_info']['responses'][sdg_number]
            else:
                response = "Please specify a valid SDG number (1-17)."
        else:
            responses = self.intents.get(intent, {}).get('responses', 
                ["I'm focused on sustainability topics. Could you rephrase that?"])
            response = random.choice(responses)
        
        if random.random() < 0.2:
            response += "\n[AI Insights] " + self._generate_ai_response(
                f"Briefly supplement this response: {response}"
            )[:120]
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def start_chat(self):
        """Start interactive chat session"""
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