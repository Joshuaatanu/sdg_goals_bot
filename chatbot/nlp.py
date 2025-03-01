import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import random

class NLPProcessor:
    def __init__(self):
        nltk.download(['punkt', 'wordnet', 'stopwords', 'punkt_tab'])
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.intents = self._load_intents()

    def _load_intents(self):
        return {
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
                'responses': [],
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

    def preprocess_text(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return tokens

    def get_intent(self, tokens):
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

    def extract_sdg_number(self, text):
        match = re.search(r'sdg (\d{1,2})|goal (\d{1,2})', text)
        if match:
            return int(match.group(1) or match.group(2))
        return None

    def postprocess_ai_response(self, response):
        prohibited_terms = ["sorry", "apologize", "as an AI"]
        if any(term in response.lower() for term in prohibited_terms):
            return "I recommend focusing on sustainable business practices. Could you clarify your question?"
        return f"{response}\n\n[AI-generated suggestion - verify with official sources]"

    def get_response(self, intent):
        responses = self.intents.get(intent, {}).get('responses', 
            ["I'm focused on sustainability topics. Could you rephrase that?"])
        return random.choice(responses) 