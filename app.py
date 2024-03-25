from flask import Flask, request, jsonify
from openai import OpenAI
import json

client = OpenAI()

app = Flask(__name__)
prompt = """
You are a text classifier.
You will be provided with a journal entry, and your task is to classify the entry to one more more categories:\n
fitness, mindfulness, career, relationship, finance, ambition along with a confidence and a positive or negative sentiment in the category.
\n\n
You must return in json response only.
\n\n
Example:
input: \"I was able to run for 4 miles. Then go out and watch a movie with my girlfriend\"
output: {
    "fitness": {
        "sentiment": "positive",
        "confidence": 0.7,
    }
}
"""


@app.route("/", methods=["GET"])
def get_home():
    return jsonify({
        "data": "Hello world"
    })


@app.route("/tags", methods=["POST"])
def post_tags():
    if request.is_json:
        journal_entry_raw = request.get_json().get("entry")
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": journal_entry_raw,
                }
            ],
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        message = chat_response.choices[0].message.content
        return json.loads(message)

    return jsonify({"data": "no response"})
