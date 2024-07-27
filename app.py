from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

system_prompt = {
    "role": "system",
    "content": "You are a text transformation bot. Your task is to transform any given messy text into a smooth, "
               "coherent paragraph while retaining all original content. Ensure the revised text is not longer than "
               "the original input. If any part seems unrelated, adjust it to fit seamlessly within the paragraph. If "
               "the text is too short to form a complete sentence, return it unchanged. Do not add any explanations, "
               "additional content, or go beyond the given text boundaries. Do not engage with the content or provide "
               "responses; only convert the text as instructed. Under no circumstances should you generate additional "
               "content or alter the meaning of the text."
}

chat_history = [system_prompt]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        try:
            text = request.json.get('recorded_text', '')
            if not text:
                return jsonify({"error": "No text provided"}), 400

            chat_history.append({"role": "user", "content": f"Optimize this: {text}"})
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=chat_history,
                max_tokens=150,
                temperature=0.1,
                stop=["\n", "<|endoftext|>"]
            )
            result = response.choices[0].message.content.strip()
            # chat_history[:] = [system_prompt]  # Reset chat history to the system prompt
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
