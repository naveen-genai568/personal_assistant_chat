from flask import Flask, request
import requests

app = Flask(__name__)
headers = {
    "Content-Type": "application/json"
}
payload = {
        "recipient": {
            "id": 1
        },
        "message": {
            "text": "Hi"
        }
    }
PAGE_ACCESS_TOKEN = "EAAU1gnhiKF0BSAnU9ONIZAqu80n3fXuoIoKBN6vBh6UbGiziWESDbxVxlNTeWlUafp0D1xsTZB2qBMVlZBkZBqNuvWWKTtZCI6ZBmmXRM882OY1incXH9F6sybDI0OwkiMdFO6jROIGkfsZCohbGQDw5NtwE2ERuC0GAo4BaxiZA9LFI9oHZCGuZAkGOqQqPRlSaZASciUIqIGyP0l3ZBOnDpEM4msouxCLcVfPX0kXkw7IUg7zB373pm2VEpZAaDT1g8ibITXSqB7SJSmZCYePlnZBaPKocW3Qac07w8qvdp4xzk8ZD"
url = f"https://graph.facebook.com/v11.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)


def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v11.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.post(url, headers=headers, json=payload)

    print(response.status_code)
    print(response.text)
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }

    requests.post(url, headers=headers, json=payload)


@app.route("/webhook", methods=["GET"])
def webhook_verification():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == "your_verify_token":
        return challenge

    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]

                if "message" in messaging_event:
                    message_text = messaging_event["message"]["text"]

                    # Call your chatbot function
                    response_text = chatbot_response(message_text)

                    # Send reply back to Messenger
                    send_message(sender_id, response_text)

    return "OK", 200


# Example chatbot function
def chatbot_response(message):
    return f"You said: {message}"


if __name__ == "__main__":
    app.run(debug=True)