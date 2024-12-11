from utils.speech import Speech
from utils.nlp import NLP
import openai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Jarvis:
    def __init__(self):
        self.speech = Speech()
        self.nlp = NLP()
        openai.api_key = 'YOUR_API_KEY'
        self.context = []  # To maintain conversation context

    def ask_gpt(self, question):
        try:
            # Maintain conversation context
            prompt = "\n".join(self.context + [f"Human: {question}", "AI:"])
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                stop=["Human:", "AI:"]
            )
            answer = response.choices[0].text.strip()
            self.context.append(f"Human: {question}")
            self.context.append(f"AI: {answer}")
            # Limit context to prevent bloating
            if len(self.context) > 10:
                self.context = self.context[-10:]
            return answer
        except Exception as e:
            logging.error(f"Error in ask_gpt: {e}")
            return "I'm having trouble thinking right now. Please try again later."

    def run(self):
        self.speech.speak("Hello! I am Jarvis. How can I assist you today?")
        while True:
            try:
                text = self.speech.listen()
                if not text:
                    continue
                
                logging.info(f"User said: {text}")
                if text.lower() in ["stop", "exit", "quit"]:
                    self.speech.speak("Goodbye!")
                    break
                
                self.speech.speak(f"You said: {text}")
                self.nlp.process_text(text)  # Example: Process commands or extract intents
                
                # Generate a response using GPT
                answer = self.ask_gpt(text)
                self.speech.speak(answer)

            except Exception as e:
                logging.error(f"Error in run loop: {e}")
                self.speech.speak("Something went wrong. Please try again.")

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
