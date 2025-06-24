# 🤖 AI-InterviewBot

AI-InterviewBot is a Streamlit-based mock interview chatbot that analyzes resumes, conducts structured technical and HR interviews, and gives final feedback. It uses Groq API (LLaMA 3), OCR, RAG pipeline with Pinecone, and LangChain for context-aware questioning.

---

## 🚀 Features

- Upload resumes in **PDF**, **Image**, or **Text** format
- Extract resume text using **Tesseract OCR**
- RAG-based question generation using **Pinecone + LangChain**
- Conducts structured interview with:
  - 5 Technical Questions
  - 5 HR Questions
- Gives detailed **feedback and selection decision**
- Secure API key management using `.env`
- Two Streamlit interfaces: `app.py` and `app1.py` for different use cases

---

## 📂 File Structure

├── app.py # Simple resume Q&A chatbot
├── app1.py # Full-featured AI Interviewer with chat
├── config.py # Interview, evaluation, and question prompts
├── rag_utils.py # RAG logic using Pinecone and LangChain
├── Main.py # Command-line interface version
├── .env # API keys (GROQ, Pinecone, etc.)
├── .gitignore # Ignore sensitive/temp files
├── README.md # Project documentation
├── requirements.txt # Python dependencies


---

## 📦 Setup Instructions

### 1. Clone the repository

`'bash
git clone https://github.com/diya268/AI-InterviewBot.git
cd AI-InterviewBot
""
# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate         # On Windows
# or
source venv/bin/activate      # On macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file

GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
NVIDIA_API_KEY=your_nvidia_api_key

# 💻 Run the App
# ▶️ Web App (Streamlit UI)

streamlit run app1.py

# ▶️ Terminal Chatbot

python Main.py

# 🧠 Tech Stack
Groq API – LLaMA 3.1 chat model

LangChain + Pinecone – Vector database & RAG

Tesseract OCR + PyMuPDF – Resume text extraction

Streamlit – Web UI

Python – Core language

# 🔐 Security Note
Do not push .env or any sensitive keys to GitHub. Add them to .gitignore.


---

### 🔹 `.gitignore`

Save as: `.gitignore`

'''gitignore
# Python cache
__pycache__/
*.py[cod]
*.so

# Environment and dependencies
.env
*.env
venv/
ENV/
env/
*.egg-info/
dist/
build/

# Logs and temp
*.log
*.tmp
*.bak

# OS/system
.DS_Store
Thumbs.db

# IDE/config
.vscode/

# Streamlit
.streamlit/

# Notebook and text
.ipynb_checkpoints/

# Optional: Rag index folder
rag_index/

# PDF/Images not needed
*.pdf
*.png
*.jpg
*.jpeg

