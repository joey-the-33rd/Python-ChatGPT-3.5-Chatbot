import os
import openai
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat():
    print("👋 Welcome to the GPT Chatbot. Type 'exit' to quit.\n")
    conversation = []``

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! 👋")
            break

        conversation.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
                messages=conversation,
                temperature=0.7
            )

            reply = response.choices[0].message.content.strip()
            conversation.append({"role": "assistant", "content": reply})
            print(f"Chatbot: {reply}")

        except Exception as e:
            print(f"⚠️ Error: {e}")
            break

if __name__ == "__main__":
    chat()
