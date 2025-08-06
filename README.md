# 🧠 Fren – Local AI Therapy Chatbot

Fren is a privacy-first, fully offline AI therapy chatbot built using the **DeepSeek LLM 7B** model, served locally through **Docker** with GPU acceleration, and powered by a lightweight **Flask** backend. Designed for real-time, empathetic conversation, Fren enables mental health support without relying on any cloud APIs or third-party services.

---

## 🚀 Features

- 🧠 **Therapy-focused LLM chat** powered by DeepSeek 7B (4-bit quantized)
- 🔐 **Fully offline and privacy-preserving** – no external API calls
- 🐳 **Containerized with Docker** for easy deployment and portability
- ⚡ **Low-latency GPU inference** with NVIDIA RTX 2060 and CUDA 11.x
- 🌐 **RESTful Flask API backend** with session-based memory
- 💬 **Responsive web frontend** using HTML, CSS, and JavaScript
- 🔁 **Multi-turn conversation support** using in-memory context
- 🧩 Extensible architecture for future integration (e.g., database, auth)

---

## 🛠️ Tech Stack

| Layer        | Tech Used |
|-------------|-----------|
| Language     | Python 3.10 |
| Backend      | Flask 2.3, flask-cors, requests |
| LLM          | DeepSeek 7B (4-bit), Ollama, PyTorch |
| Containerization | Docker, Docker Compose |
| Hardware      | NVIDIA RTX 2060 (6GB), CUDA 12.8 |
| Frontend      | HTML5, CSS3, JavaScript (ES6) |
| API Format    | RESTful JSON |

---

## 🧪 How It Works

1. **Model Deployment**  
   - DeepSeek LLM 7B is served locally via **Ollama** in a Docker container using GPU acceleration for fast inference.

2. **Backend API**  
   - A **Flask server** exposes RESTful endpoints (`/chat`, `/health`) for frontend interaction and LLM communication using the `requests` module.

3. **Conversation Management**  
   - Python in-memory storage simulates **session-based memory**, preserving prompt context for multi-turn chat.

4. **Frontend**  
   - A minimal HTML/CSS/JS interface handles user input and displays bot responses using asynchronous `fetch()` requests.

---

## 📦 Installation & Setup

> 🧠 **Requirements**: Linux, Docker, NVIDIA GPU w/ drivers, Python 3.10+

```bash
# 1. Clone the repo
git clone https://github.com/Paras911/fren
cd fren

# 2. Start the LLM (Ollama must be installed)
ollama run deepseek:7b

# 3. (Optional) Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Run the Flask backend
python app.py
