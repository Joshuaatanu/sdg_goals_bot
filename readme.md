# AISustainabilityChatbot

## Overview

The AISustainabilityChatbot is an interactive chatbot designed to provide information and advice on sustainability practices and the United Nations Sustainable Development Goals (SDGs). It utilizes natural language processing (NLP) to understand user queries and generate responses using Google's Gemini API.

## Features

- Provides information on sustainability practices.
- Offers insights into the 17 Sustainable Development Goals (SDGs).
- Engages users in a conversational manner.
- Utilizes NLP for intent recognition and response generation.

## Requirements

- Python 3.7 or higher
- Google Gemini API key
- NLTK library for natural language processing

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Joshuaatanu/sdg_goals_bot.git
   cd sdg_goals_bot
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Google Gemini API key:**

   Create a `.env` file in the root directory of the project and add your Gemini API key:

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

To start the chatbot, run the following command:

```bash
python main.py
```

Once the chatbot is running, you can interact with it by typing your queries related to sustainability. Type `exit`, `quit`, or `bye` to end the conversation.

## Code Structure

- `chatbot/`
  - `chatbot.py`: Contains the main chatbot logic.
  - `nlp.py`: Handles natural language processing tasks.
  - `sdg.py`: Manages information related to the Sustainable Development Goals.
  - `generative_ai.py`: Interacts with the Google Gemini API to generate responses.
- `main.py`: Entry point to start the chatbot.
- `.env`: Environment variables for sensitive information.
- `requirements.txt`: List of required Python packages.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- [Google Gemini](https://cloud.google.com/genai) for providing the Gemini API.
- [NLTK](https://www.nltk.org/) for natural language processing tools.