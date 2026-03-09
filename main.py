from flask import Flask, request, jsonify, render_template
import dashscope
import os
from dotenv import load_dotenv
from memory import save_message, get_history

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Setup API Key
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# Load prompt and knowledge files
with open("siggy_prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

with open("ritual_docs_full.txt", "r", encoding="utf-8") as f:
    docs = f.read()

with open("dataset_qa.txt", "r", encoding="utf-8") as f:
    dataset = f.read()

# Home route (Chat UI)
@app.route("/")
def home():
    return render_template("index.html")


# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.json

        user_id = data.get("user_id", "default")
        message = data.get("message", "")

        # Get conversation history
        history = get_history(user_id)

        conversation_context = ""

        for h in history:
            conversation_context += f"User: {h['user']}\nSiggy: {h['assistant']}\n"

        # Build system prompt
        system_prompt = f"""
{prompt}

Ritual Documentation:
{docs}

Dataset Knowledge:
{dataset}

Conversation History:
{conversation_context}
"""

        # Call Qwen model
        response = dashscope.Generation.call(
            model="qwen-plus",
            prompt=f"{system_prompt}\nUser: {message}\nSiggy:"
        )

        reply = response["output"]["text"]

        # Save conversation
        save_message(user_id, message, reply)

        return jsonify({
            "response": reply
        })

    except Exception as e:

        return jsonify({
            "response": "Oops, something went wrong while talking to Siggy.",
            "error": str(e)
        })


# Run server
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 3000))

    app.run(host="0.0.0.0", port=port)
