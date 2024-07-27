from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

system_prompt = {
    "role": "system",
    "content": "The Speech-to-Text Pause Smoothing Specialist is an AI agent designed to enhance the readability of "
               "transcribed speech by smoothing out pauses while keeping the original content intact.\n"
               "This AI agent processes raw speech-to-text transcriptions, identifies pauses, and ensures the text "
               "flows naturally without altering the original words. The agent's priority is to convert the speech "
               "into a smooth and understandable format while maintaining the original context, without mumbling or "
               "explaining. The agent simply returns the smoothed response.\n"
               "Simply return the smoothed response without any additional explanations or mumbling."
}

# Initialize the chat history
chat_history = [system_prompt]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        text = request.json.get('recorded_text', '')
        chat_history.append({"role": "user", "content": text})
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=chat_history,
            max_tokens=100,
            temperature=1.2
        )
        result = {"message": response.choices[0].message.content}
        return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
