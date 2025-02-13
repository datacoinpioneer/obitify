import openai
import spacy
from flask import Flask, request, jsonify, render_template
import json
import ssl
import requests
import os

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Create an SSL context to disable certificate verification
context = ssl._create_unverified_context()

# Set the context to the openai.api_requestor session
#openai.api_requestor._session.verify = False

# OpenAI GPT-3 API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Flask app setup
app = Flask(__name__)

# Predefined set of questions for the interview
questions = [
    "What is the purpose of the application or website?",
    "Who is the target audience?",
    "What features are required in the first version?",
    "Are there any key performance metrics to consider?",
    "Are there any technical requirements (e.g., platform, integrations)?",
    "What are the business goals or KPIs for this project?"
]

# Function to analyze responses using spaCy for named entity recognition
def analyze_response(response):
    doc = nlp(response)
    entities = {"features": [], "platforms": [], "goals": []}
    
    for ent in doc.ents:
        if ent.label_ == "PRODUCT":
            entities["features"].append(ent.text)
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            entities["platforms"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["goals"].append(ent.text)
    
    return entities

# Function to generate follow-up questions using GPT-3
def get_follow_up_question(context):
    prompt = f"Given the following statement, suggest a follow-up question to clarify: '{context}'"
    
    # Define the headers and payload for the OpenAI API call
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "max_tokens": 60,
        "model": "gpt-4o-mini",
        "store": True,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    #response = openai.Completion.create(
    #    engine="text-davinci-003",
    #    prompt=prompt,
    #    max_tokens=60
    #)

    # Make the API call using requests (with SSL verification disabled)
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload),
        verify=False  # Disable SSL certificate verification
    )

    # Print the response from OpenAI
    if response.status_code == 200:
        print("OpenAI API Response:")
        print(response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return response.json()['choices'][0]['message']['content'].strip()

# Route for serving the index.html page
@app.route("/")
def home():
    return render_template("index.html")

# Route for starting the interview with the first question
@app.route("/start_interview", methods=["GET"])
def start_interview():
    # Start with the first question
    return jsonify({"question": questions[0], "question_number": 1})

# Route for handling stakeholder responses
@app.route("/submit_response", methods=["POST"])
def submit_response():
    data = request.json
    response = data.get("response")
    question_number = data.get("question_number")
    
    # Analyze the response
    entities = analyze_response(response)
    
    # Generate follow-up questions if necessary
    follow_up_question = None
    if "features" not in entities or not entities["features"]:
        follow_up_question = get_follow_up_question(response)
    
    # Extracted data to store in a structured format
    interview_data = {
        "response": response,
        "entities": entities,
        "follow_up_question": follow_up_question
    }
    
    # Store the response data in a JSON file
    with open("interview_data.json", "a") as f:
        json.dump(interview_data, f, indent=4)
        f.write("\n")
    
    # Check if there are more questions or if the interview is complete
    if question_number < len(questions):
        return jsonify({"question": questions[question_number], "question_number": question_number + 1, "follow_up_question": follow_up_question})
    else:
        return jsonify({"message": "Interview complete. Thank you!"})

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
