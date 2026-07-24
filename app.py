from flask import Flask, request, jsonify, render_template
from scripts.nlp_engine import predict_intent
from scripts.api_integration import get_weather, get_news
from scripts.task_manager import add_reminder, view_reminders, delete_reminder
import logging

logging.basicConfig(filename='chatbot.log',level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("/workspaces/personal_assistant_chat/template/index.html")

feedback_data=[]
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    intent = predict_intent(user_input)

    if intent == "greeting":
        response = "Hello! How can I assist you today?"

    elif intent == "goodbye":
        response = "Goodbye! Have a great day!"

    elif intent == "weather":
        city = request.json.get('city')
        response = get_weather(city)

    elif intent == "reminder":
        reminder_text = request.json.get('reminder_text')
        reminder_time = request.json.get('reminder_time')
        response = add_reminder(reminder_text, reminder_time)

    elif intent == "view_reminders":
        response = view_reminders()

    elif intent == "delete_reminder":
        reminder_text = request.json.get('reminder_text')
        response = delete_reminder(reminder_text)
    
    elif intent == "news":
        response = get_news()

    else:
        response = "I'm sorry, I don't understand that. Can you please rephrase?"

    return jsonify({"response": response})
    logging.info(f"User Input: {user_input}, predicted intent: {intent}, Response: {response}")

@app.route("/feedback", methods=['POST'])
def feedback():
    user_feedback = request.json
    feedback_data.append(user_feedback)

    return jsonify({"message": "Thank you for your feedback!"})
if __name__ == "__main__":
    app.run(debug=True)