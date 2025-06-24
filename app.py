import streamlit as st
from groq import Groq

# Groq API key (keep this secure in production)
API_KEY = "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"

# Resume context
RESUME_CONTEXT = """
Diya Shah
Contact: +918128426803, Shahdia2630@gmail.com, LinkedIn: Diya Shah
Summary: AI developer skilled in machine learning, deep learning, and NLP. Experienced in building chatbots and recommendation systems using LSTM and Random Forest. Proficient in Python, TensorFlow, data preprocessing, model deployment, and performance optimization for actionable insights.
Technical Skills:
Programming Languages: Python, Java, SQL, HTML, CSS, JavaScript
Tools: VS Code, PyCharm, GitHub, Jupyter Notebook, Google Colab, PowerBI, Excel
Soft Skills: Communication, Time Management, Presentation, Leadership
Experience:
Data Science Intern, Tech Elecon Pvt. Ltd., Anand, Gujarat (Dec 2024–May 2025): Developed AI-powered HRMS chatbot, integrated NLP and LLM models, improved response time by 60% and reduced HR workload by 40%.
Data Science and Machine Learning Intern, BrainyBeam Info-Tech, Ahmedabad, Gujarat (May 2024–Jun 2024): Built Car4u, a car recommendation system using Random Forest and XGBoost for personalized recommendations.
Projects:
Invoice Data Extraction (Python, YOLOv8, OCR-Tesseract, Django): Automated invoice data extraction with OCR and NLP, improved accuracy, reduced processing time by 60%.
Stock Price Prediction (Python, LSTM, Streamlit): Developed LSTM-based stock price prediction model with sentiment analysis.
Education: B.Tech in Artificial Intelligence and Data Science, A.D. Patel Institute of Technology (2021–2025), CPI: 8.07.
Certifications: Introduction to Machine Learning (Duke University), IBM Data Science Professional Certificate.
"""

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Streamlit UI
st.set_page_config(page_title="Resume Chatbot - Diya Shah", layout="centered")
st.title("🤖 Grok - Your Resume Assistant")
st.markdown("Ask me anything about **Diya Shah**")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chatbot function
def ask_groq(question):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"Hi! I'm Grok, your assistant, here to help you learn about Diya Shah, a talented AI developer. I've got all the details about her skills, experience, projects, and qualifications. Answer questions based on this resume context: {RESUME_CONTEXT}."
            },
            {
                "role": "user",
                "content": question,
            }
        ]
    )
    return response.choices[0].message.content

# User input
user_input = st.chat_input("Type your question here...")

# Handle chat
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        answer = ask_groq(user_input)
    st.session_state.chat_history.append(("bot", answer))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
