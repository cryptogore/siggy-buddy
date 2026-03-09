from flask import Flask, request, jsonify, render_template
import dashscope
import os
from memory import save_message, get_history

app = Flask(__name__)

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

prompt = open("siggy_prompt.txt").read()
docs = open("ritual_docs_full.txt").read()
dataset = open("dataset_qa.txt").read()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    user_id = data.get("user_id","default")

    message = data["message"]

    history = get_history(user_id)

    context = ""

    for h in history:
        context += f"User: {h['user']}\nSiggy: {h['assistant']}\n"

    system_prompt = f"""
{prompt}

Knowledge:
{docs}

Dataset:
{dataset}

Conversation history:
{context}
"""

    response = dashscope.Generation.call(
        model="qwen-plus",
        prompt=f"{system_prompt}\nUser: {message}\nSiggy:"
    )

    reply = response["output"]["text"]

    save_message(user_id, message, reply)

    return jsonify({"response": reply})


app.run(host="0.0.0.0", port=3000)