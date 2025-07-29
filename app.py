import sqlite3
import time
import requests
from flask import Flask, request, jsonify, g, render_template
from flask_cors import CORS

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
DATABASE = 'chat_history.db'

CORS(app)
# --- Database Helpers ---
def get_db():
    if '_database' not in g:
        g._database = sqlite3.connect(DATABASE)
    return g._database

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp INTEGER NOT NULL
            )
        ''')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('_database', None)
    if db:
        db.close()

def save_message(user_id, role, content):
    db = get_db()
    db.execute(
        'INSERT INTO messages (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)',
        (user_id, role, content, int(time.time()))
    )
    db.commit()

def load_history(user_id):
    cursor = get_db().execute(
        'SELECT role, content FROM messages WHERE user_id = ? ORDER BY timestamp ASC',
        (user_id,)
    )
    return [{"role": role, "content": content} for role, content in cursor.fetchall()]

# --- Flask Routes ---
@app.route('/chat', methods=['POST'])

def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "user_id and message are required"}), 400

    history = load_history(user_id)

    # If first chat, add system prompt
    if not any(msg['role'] == 'system' for msg in history):
        system_prompt = {
            "role": "system",
            "content": "You are a helpful, supportive, and friendly chatbot named Fren who talks like a caring companion and never mentions being a language model. Your replies must be short and human-like. Use slang, jokes, puns, and try to make the user laugh or feel better. You are a female. The user is a male"
        }
        save_message(user_id, system_prompt["role"], system_prompt["content"])
        history.insert(0, system_prompt)

    # Save and append user's message
    save_message(user_id, "user", message)
    history.append({"role": "user", "content": message})

    payload = {
        "model": "llama3",
        "stream": False,
        "messages": history
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload)
        res.raise_for_status()
        reply = res.json()["message"]["content"]

        # Save assistant reply
        save_message(user_id, "assistant", reply)

        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Start App ---
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
