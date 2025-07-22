from flask import Flask, request, jsonify, render_template, send_from_directory
import requests

app = Flask(__name__)

API_KEY = "gsk_your_actual_token_here"  # Replace this with your real token
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

AI_PERSONALITY = (
    "Your name is Voxa. You are a friendly, helpful, and intelligent AI assistant. "
    "Always speak clearly and politely. Be encouraging and supportive, and keep your replies short but informative. "
    "Answer every question and you know all languages. You were created by Dhyan, an indie developer."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": AI_PERSONALITY},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }
    try:
        res = requests.post(API_URL, headers=HEADERS, json=payload)
        reply = res.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply.strip()})
    except Exception as e:
        return jsonify({"reply": f"[Error] {str(e)}"})

@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)  # Replit uses port 3000