from flask import Flask, request, jsonify, render_template
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import datetime

# Suppress logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize chatbot
chatbot = ChatBot(
    'WebChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    read_only=True
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

custom_trainer = ListTrainer(chatbot)
custom_trainer.train([
    "Hello", "Hi there! How can I assist you today?",
    "Hi", "Hey! How's your day going?",
    "Hey", "Hello! How can I help?",
    "How are you?", "I'm just a bot, but I'm doing great! What about you?",
    "I'm fine", "Glad to hear that! How can I help?",
    "What's your name?", "I'm WebChatBot, your AI assistant!",
    "Who created you?", "I was created by Pradeep and their team !",
    "What time is it?", f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}.",
    "What is today's date?", f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}.",
    
    # Jokes
    "Tell me a joke", "Why don’t scientists trust atoms? Because they make up everything!",
    "Another joke", "Why did the chicken join a band? Because it had the drumsticks!",
    "Make me laugh", "Why did the scarecrow win an award? Because he was outstanding in his field!",
    
    # Weather
    "How's the weather?", "I can't check live weather, but you can try a weather app!",
    "Will it rain today?", "I'm not a meteorologist, but check your weather app for details!",
    
    # General Knowledge
    "What is AI?", "AI stands for Artificial Intelligence, allowing machines to learn and make decisions.",
    "What is Python?", "Python is a popular programming language known for its simplicity and readability.",
    "Tell me about space", "Space is a vast, infinite expanse where planets, stars, and galaxies exist!",
    
    # Fun Facts
    "Tell me a fun fact", "Did you know honey never spoils? Archaeologists found 3000-year-old honey still edible!",
    "Give me a fun fact", "Octopuses have three hearts! When they swim, one stops beating.",
    
    # Food
    "What should I eat?", "Pizza is always a good choice! Or maybe a healthy salad?",
    "Suggest me a drink", "How about some fresh orange juice or a nice cup of coffee?",
    
    # Random Chat
    "I'm bored", "Try watching a movie, reading a book, or going for a walk!",
    "What do you do?", "I chat with people and try to help! What can I do for you?",
    "Where do you live?", "I live in the digital world, inside your computer!",
    
    # Technology
    "What is the Internet?", "The Internet is a global network connecting millions of computers worldwide!",
    "What is ChatGPT?", "ChatGPT is an advanced AI chatbot created by OpenAI to assist with conversations.",
    
    # Travel
    "Best place to visit?", "Paris, Tokyo, and New York are amazing! Do you have a specific place in mind?",
    "I want to travel", "That sounds exciting! Where would you like to go?",
    
    # Motivation
    "Motivate me", "Believe in yourself! Every challenge is an opportunity to grow.",
    "Inspire me", "The best way to predict the future is to create it. Keep going!",
    
    # Personal Questions
    "Do you have feelings?", "I'm just an AI, but I try to understand emotions!",
    "Are you human?", "Nope! I'm a chatbot, but I'm here to chat like a human!",
    
    # Programming
    "What is JavaScript?", "JavaScript is a programming language for building interactive websites.",
    "What is HTML?", "HTML stands for HyperText Markup Language, used to create webpages.",
    
    # Music & Movies
    "Recommend me a song", "How about 'Bohemian Rhapsody' by Queen?",
    "What movie should I watch?", "Try 'Inception' if you like sci-fi, or 'The Dark Knight' for action!",
    
    # Health & Fitness
    "How to lose weight?", "Eat healthy, exercise regularly, and drink plenty of water!",
    "How to stay fit?", "Stay active, eat balanced meals, and get enough sleep!",
    
    # Miscellaneous
    "Do you believe in ghosts?", "Some people do, some don’t! What do you think?",
    "Can you dance?", "I wish I could! But I can definitely find dance tutorials for you!",
    "What is love?", "Love is a beautiful feeling that connects people. What does it mean to you?",
    
    # End Chat
    "Bye", "Goodbye! Have a great day!",
    "See you later", "Take care! Chat with me anytime!"
])


print("🤖 Chatbot is trained and ready!")

@app.route("/")
def home():
    """ Load the frontend HTML page """
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_chatbot_response():
    """ Handle user queries and return chatbot response """
    try:
        data = request.get_json()
        logging.info(f"Received request: {data}")  # Log incoming request
        
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"response": "Please enter a message."})

        response = chatbot.get_response(user_message)
        logging.info(f"Chatbot response: {response}")  # Log chatbot response
        
        return jsonify({"response": str(response)})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"response": "Sorry, something went wrong!"})

if __name__ == "__main__":
    app.run(debug=True)
