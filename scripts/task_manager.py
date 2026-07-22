import json
from datetime import datetime

# Load reminders from file
def load_reminders():
    try:
        with open("/workspaces/personal_assistant_chat/data/reminders.json", "r") as file:
            reminders = json.load(file)
    except FileNotFoundError:
        reminders = []
    return reminders


# Save reminders to file
def save_reminders(reminders):
    with open("/workspaces/personal_assistant_chat/data/reminders.json", "w") as file:
        json.dump(reminders, file, indent=4)


# Add a new reminder
def add_reminder(reminder_text, reminder_time):
    reminders = load_reminders()

    reminder = {
        "text": reminder_text,
        "time": reminder_time
    }

    reminders.append(reminder)
    save_reminders(reminders)

    return "Reminder added successfully."


# View all reminders
def view_reminders():
    reminders = load_reminders()

    if not reminders:
        return "You have no reminders."

    reminders_str = "\n".join(
        [f"{reminder['time']}: {reminder['text']}" for reminder in reminders]
    )

    return f"Your reminders:\n{reminders_str}"


# Delete a reminder
def delete_reminder(reminder_text):
    reminders = load_reminders()

    reminders = [
        reminder for reminder in reminders
        if reminder["text"] != reminder_text
    ]

    save_reminders(reminders)

    return "Reminder deleted successfully."


# Test the task manager functions
if __name__ == "__main__":
    print(add_reminder("Buy groceries", "2024-06-27 18:00"))
    print(view_reminders())
    print(delete_reminder("Buy groceries"))
    print(view_reminders())