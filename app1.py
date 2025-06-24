import streamlit as st
from groq import Groq
from io import StringIO
import pandas as pd
import pytesseract
from pdf2image import convert_from_path
import tempfile
import fitz  # PyMuPDF
from PIL import Image
from config import InterviewPrompt, QuestionsPrompt  ,EvaluationPrompt
from rag_utils import get_rag_pipeline

# ========== Configuration ==========
API_KEY = GROQ_API_KEY
MODEL_NAME = "llama-3.1-8b-instant"

# ========== Initialize ==========
client = Groq(api_key=API_KEY)

# Set up Streamlit page configuration
st.set_page_config(page_title="Chatbot", page_icon="", layout="centered")

# ========== Session State ==========
if "chat_history" not in st.session_state:
    user_name = st.session_state.get("user_name", None)
    if user_name:
        greeting =(""" 
            f"👋 Hiii, {user_name}, welcome to AI interviewbot. Let's start with the mock interview session.\n\n"
        Let's begin the interview. I'll ask the questions one by one, and you can respond accordingly.
        Introduction Question
        Can you tell me about your background and how you became interested in AI development?
        """    
        )
        st.session_state.chat_history = [("bot", greeting)]
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Sidebar: Upload resume file
st.sidebar.header("\U0001F4C4 Upload Resume")
uploaded_file = st.sidebar.file_uploader(
    "Upload your resume (PDF, image, or text format)", 
    type=["pdf", "png", "jpg", "jpeg", "txt"]
)

if not uploaded_file:
    st.sidebar.info("Please upload a resume to begin chatting.")

# Extract text from uploaded file
def extract_resume_text(file, filetype):
    if file is not None:
        if filetype == "pdf":
            doc = fitz.open(stream=file.read(), filetype="pdf")
            full_text = ""
            for page in doc:
                text = page.get_text()
                if not text.strip():  # if empty, fallback to OCR
                    img = page.get_pixmap(dpi=300)
                    text = pytesseract.image_to_string(img.tobytes("ppm"))
                full_text += text + "\n"
            return full_text.strip()
        elif filetype in ["png", "jpg", "jpeg"]:
            pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            image = Image.open(file)
            return pytesseract.image_to_string(image)
        elif filetype == "txt":
            return StringIO(file.getvalue().decode("utf-8")).read()
    return None

def extract_name_from_resume(resume_text):
    # Simple heuristic: first non-empty line is the name
    for line in resume_text.splitlines():
        line = line.strip()
        if line:
            return line
    return "Candidate"

# If file uploaded, extract and store text
if uploaded_file:
    file_type = uploaded_file.type.split("/")[-1]
    extracted_text = extract_resume_text(uploaded_file, file_type)
    if extracted_text:
        st.session_state.resume_text = extracted_text
        # Extract and store the user's name
        st.session_state.user_name = extract_name_from_resume(extracted_text)
        get_rag_pipeline().upsert_resume(extracted_text)  # RAG embedding with Multilingual-e5-large model
        st.sidebar.success("Resume uploaded and processed successfully!")

# ========== State Initialization ==========
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "chat_history" not in st.session_state:
    user_name = st.session_state.get("user_name", None)
    if user_name:
        greeting = ( 
            f"👋 Hiii, {user_name}, welcome to AI interviewbot. Let's start with the mock interview session.\n\n"
            "Let's begin the interview. I'll ask the questions one by one, and you can respond accordingly.\n"
            "Introduction Question\n"

            "Can you tell me about your background and how you became interested in AI development?\n " 
    )
        st.session_state.chat_history = [("bot", greeting)]

# ========== Chatbot Logic ==========
def ask_groq(user_input, resume_context):
    if not resume_context:
        return "Please upload a resume first in the sidebar to proceed."

    # Ensure user_input is a string
    if not isinstance(user_input, str):
        user_input = str(user_input)

    retrieved_context = get_rag_pipeline().retrieve_context(user_input, k=3)

    interview_instructions = InterviewPrompt.INSTRUCTIONS 
    prompt = f"""
    You are an AI Interviewer conducting a professional interview based on the candidate's resume.
    
    Resume:
    {resume_context}

    User Input:
    {user_input}

    Your task:
    - Ask a total of 10 questions: 5 technical questions and 5 HR questions.
    - Ask the questions one by one, waiting for the candidate's answer before moving to the next question.
    - Number each question sequentially from 1 to 10.
    - Do NOT repeat any question or number.
    - After all 10 questions are answered, provide feedback and a final thank you message.
    - Do not ask multiple questions at once; only ask the next question after the candidate responds.
    - If user say "exit' then give the feedback to the user and the final decision and then print the final thank you prompt.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": interview_instructions,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.01,
        max_tokens=512,
    )
    return response.choices[0].message.content

# ========== UI Layout ==========
st.markdown(
    """
    <h1 style='text-align: center;'>InterviewBot - AI Interview Assistant </h1>
    """,
    unsafe_allow_html=True
)
st.divider()    

# ========== Main Chat Interface ==========
if st.session_state.resume_text:
    user_prompt = st.chat_input("You (Candidate):")

    if user_prompt:
        st.session_state.chat_history.append(("user", user_prompt))

 #       if user_prompt.lower().strip() in ["hi", "hello", "hii", "hey"]:
#            user_prompt = "Start the interview with a very beginner-level introduction question always."
        import time
        start = time.time()
        bot_reply = ask_groq(user_prompt, st.session_state.resume_text)
        print("Groq API call took", time.time() - start, "seconds")
        
        st.session_state.chat_history.append(("bot", bot_reply))

    if st.session_state.chat_history:
        for sender, message in st.session_state.chat_history:
            if sender == "user":
                st.chat_message("user").markdown(message)
            else:
                st.chat_message("assistant").markdown(message)
        st.divider()
else:
    st.info("Please upload your resume to begin the interview.")

delete_clicked = st.sidebar.button("Delete Resume & Chunks")
if delete_clicked:
    get_rag_pipeline().clear_index()
    st.session_state.resume_text = None
    st.session_state["uploaded_file"] = None  # Clear uploaded file from session state
    st.sidebar.success("Resume and its chunks deleted from the database.")
