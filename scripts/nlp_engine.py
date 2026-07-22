import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
import json
import random
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    text = text.lower()

    tokens = nltk.word_tokenize(text)

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in string.punctuation and word not in stop_words
    ]

    return " ".join(tokens)

# Create models directory
os.makedirs("models", exist_ok=True)

# Load the intents file
with open("/workspaces/personal_assistant_chat/data/intents.json", "r") as file:
    intents = json.load(file)

# Extract patterns and corresponding tags
patterns = []
tags = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        processed = preprocess_text(pattern)
        patterns.append(processed)
        tags.append(intent["tag"])
        # patterns.append(pattern)
        # tags.append(intent["tag"])

# Encode the tags
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(tags)

# Vectorize the patterns
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns).toarray()
y = np.array(labels)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

from imblearn.over_sampling import SMOTE

print(f"Missing values: {np.isnan(X).sum()}")

X = np.nan_to_num(X)

smote = SMOTE(random_state=42)

X_resampled, Y_resampled = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_resampled,Y_resampled, test_size = 0.2, random_state=42)


# Build the model
model = Sequential()

model.add(
    Dense(
        128,
        input_shape=(X_train.shape[1],),
        activation="relu"
    )
)

model.add(Dropout(0.5))

model.add(
    Dense(
        64,
        activation="relu"
    )
)

model.add(Dropout(0.5))

model.add(
    Dense(
        len(label_encoder.classes_),
        activation="softmax"
    )
)

# Compile the model
model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam",
    metrics=["accuracy"]
)

# Train the model
model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=8,
    verbose=1,
    validation_data=(X_test, y_test)
)

y_pred = model.predict(X_test),
y_pred_classes = np.argmax(y_pred, axis=1)
# print(classification_report(y_test, y_pred_classes, target_names = label_encoder.classes_))


# model.fit()

# Save the model
model.save("models/nlp_model.keras")

# Save the vectorizer
with open("models/tokenizer.pickle", "wb") as file:
    pickle.dump(vectorizer, file)

# Save the label encoder
with open("models/label_encoder.pickle", "wb") as file:
    pickle.dump(label_encoder, file)

print("Training completed successfully.")
print("Model saved to models/nlp_model.keras")
print("Vectorizer saved to models/tokenizer.pickle")
print("Label encoder saved to models/label_encoder.pickle")



# Load intents
with open("/workspaces/personal_assistant_chat/data/intents.json", "r") as file:
    intents = json.load(file)

# Initialize lemmatizer


# Preprocess text
# def preprocess_text(text):
#     text = text.lower()

#     tokens = nltk.word_tokenize(text)

#     tokens = [
#         lemmatizer.lemmatize(word)
#         for word in tokens
#         if word not in string.punctuation
#         and word not in stop_words
#     ]

#     return " ".join(tokens)


# Predict intent
def predict_intent(text):
    processed = preprocess_text(text)

    vector = vectorizer.transform([processed]).toarray()

    prediction = model.predict(vector, verbose=0)

    index = np.argmax(prediction)

    return label_encoder.inverse_transform([index])[0]


# Get response
def get_response(intent_tag):
    for intent in intents["intents"]:
        if intent["tag"] == intent_tag:
            return random.choice(intent["responses"])

    return "Sorry, I don't understand."


# Chat loop
print("Personal Assistant Chatbot")
print("Type 'quit' to exit.")
intent = predict_intent("remainder")
response = get_response(intent)
print("Intent :", intent)
print("Bot    :", response)

# while True:
#     user_input = input("\nYou: ")

#     if user_input.lower() == "quit":
#         print("Bot: Goodbye!")
#         break

    # intent = predict_intent(user_input)
    # response = get_response(intent)

    