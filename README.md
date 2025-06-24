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

