from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

dog_facts = {
    "what fun facts about dogs?": [
        "Did you know a dog's sense of smell is 10,000 to 100,000 times stronger than a human's?",
        "There are over 200 recognized dog breeds in the world!",
        "Dogs' nose prints are as unique as human fingerprints and can be used to identify them.",
        "Dogs have three eyelids, including one to keep their eyes moist and protected."
    ],
    "interesting facts about dogs": [
        "The Basenji is the only dog breed that can't bark, but they can yodel!",
        "Dalmatians are born completely white and develop their spots as they grow older."
    ],
    "why are dogs' noses wet?": [
        "Dogs' noses secrete a thin layer of mucous that helps them absorb scent chemicals."
    ]
    # Add more questions and answers as needed
}


def preprocess_text(text):
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(w.lower()) for w in text.split() if w not in stop_words])

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    preprocessed_question = preprocess_text(question).lower()
    dog_keywords = ["dog", "dogs", "canine", "puppies"]

    # Extract keywords from the user's question
    question_tokens = word_tokenize(preprocessed_question)
    question_keywords = [word for word in question_tokens if word in dog_keywords]

    if question_keywords:
        for fact_question, answers in dog_facts.items():
            # Check if any keywords match with the fact questions
            fact_tokens = word_tokenize(fact_question.lower())
            if any(keyword in fact_tokens for keyword in question_keywords):
                return random.choice(answers)

    return "I don't seem to know any dog facts related to that. Ask me something else!"
# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.write("Hi there! Welcome to the Dog Fact Chat. Ask me anything about dogs!")
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    st.write(response)
    st.session_state['chat_history'].append(("Bot", response))
st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
