import json
import sqlite3
import speech_recognition as sr
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize SQLite Database
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, user TEXT, bot TEXT)")
conn.commit()

# Gemini AI API (Replace with actual API key)
GEMINI_API_KEY = "YOUAIzaSyAFTOY6lKnirwFmmxKsNeBDZ8l36KurUbU"
GEMINI_URL = "https://api.gemini.com/v1/chat"

# Function to process AI response
def get_ai_response(user_input):
    payload = {"message": user_input}
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    response = requests.post(GEMINI_URL, json=payload, headers=headers)
    return response.json().get("reply", "I'm sorry, I don't understand.")

# Speech Recognition
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

# API Route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]
    
    bot_response = get_ai_response(user_message)

    cursor.execute("INSERT INTO chats (user, bot) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    
    return jsonify({"reply": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
