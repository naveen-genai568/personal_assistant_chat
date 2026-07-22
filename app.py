from flask import Flask, request, jsonify
from scripts.nlp_engine import predict_intent
from scripts.api_integration import get_weather
from scripts.task_manager import add_reminder, view_reminders, delete_reminder

app = Flask(__name__)

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

    else:
        response = "I'm sorry, I don't understand that. Can you please rephrase?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)