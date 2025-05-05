import os
import openai
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Text-to-Speech
engine = pyttsx3.init()

# GPT Chat Function
def get_gpt_reply(conversation):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

# Text-to-Speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Chat Handler
conversation = [{"role": "system", "content": "You are a helpful assistant."}]

def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return

    chat_log.insert(tk.END, f"You: {user_input}\n")
    entry.delete(0, tk.END)
    conversation.append({"role": "user", "content": user_input})

    reply = get_gpt_reply(conversation)
    conversation.append({"role": "assistant", "content": reply})
    chat_log.insert(tk.END, f"Bot: {reply}\n")
    speak(reply)

def voice_input():
    try:
        user_input = recognize_speech()
    except Exception as e:
        user_input = f"Error recognizing speech: {e}"
    entry.delete(0, tk.END)
    entry.insert(0, user_input)
    send_message()

# GUI Setup
root = tk.Tk()
root.title("GPT Voice Chatbot")

chat_log = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
chat_log.pack(padx=10, pady=10)

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5, fill=tk.X)

entry = tk.Entry(input_frame, width=50)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_btn = tk.Button(input_frame, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT, padx=(5, 0))

voice_btn = tk.Button(input_frame, text="🎤 Speak", command=voice_input)
voice_btn.pack(side=tk.LEFT, padx=(5, 0))

root.mainloop()
