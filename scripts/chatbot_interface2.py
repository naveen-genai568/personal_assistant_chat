from flask import Flask, request, jsonify
import requests
import os
from nlp_engine import predict_intent
from api_integration import get_weather
from task_manager import (
    add_reminder,
    view_reminders,
    delete_reminder
)

app = Flask(__name__)

# ==========================
# Configuration
# ==========================
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_verify_token_123")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "YOUR_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID")

def chatbot_response(user_input):
    intent = predict_intent(user_input)

    if intent == "greeting":
        return "Hello! How can I assist you today?"

    elif intent == "goodbye":
        return "Goodbye! Have a great day!"

    elif intent == "weather":
        return "Which city would you like the weather update for?"

    elif intent == "reminder":
        return "What would you like to be reminded about and when?"

    elif intent == "knowledge":
        return "Here's a fun fact: Did you know that honey never spoils?"

    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"


# Test the chatbot interface
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("ChatBot: Goodbye! Have a great day!")
        break

    response = chatbot_response(user_input)
    print(f"ChatBot: {response}")