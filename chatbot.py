import os
import openai
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()  # type: ignore
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat():
    """
    Run the GPT Chatbot in the terminal.

    This function provides a command-line interface to interact with the GPT-3.5 model.
    It maintains a conversation context and generates responses based on the user's input.
    The user can exit the chatbot by typing 'exit' or 'quit'.

    Example interaction:

    $ python -m chatbot
    Welcome to the GPT Chatbot. Type 'exit' to quit.
    """
    print("👋 Welcome to the GPT Chatbot. Type 'exit' to quit.\n")
    conversation = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! 👋")
            break

        conversation.append({"role": "user", "content": user_input})

        try:
            response = openai.chat.completions.create(  # type: ignore
                model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
                messages=conversation,
                temperature=0.7
            )

            reply = (response.choices[0].message.content or "").strip()  # type: ignore
            conversation.append({"role": "assistant", "content": reply})
            print(f"Chatbot: {reply}")

        except Exception as e:
            print(f"⚠️ Error: {e}")
            break

if __name__ == "__main__":
    chat()
