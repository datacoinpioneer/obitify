import openai
import spacy
from flask import Flask, request, jsonify
import json

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# OpenAI GPT-3 API key
openai.api_key = "your_openai_api_key"

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
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60
    )
    return response.choices[0].text.strip()

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
        return jsonify({"question": questions[question_number], "question_number": question_number + 1})
    else:
        return jsonify({"message": "Interview complete. Thank you!"})

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)