import os
from groq import Groq
import pytesseract
from pdf2image import convert_from_path


# Configure path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    resume_text = ""
    for img in images:
        resume_text += pytesseract.image_to_string(img)
    return resume_text

# Step 1: Store the resume context
#RESUME_CONTEXT = """
   #Diya Shah
   #AI developer skilled in machine learning, deep learning, and NLP. 
   #Experience: Data Science Intern at Tech Elecon Pvt. Ltd. (AI-powered HRMS chatbot, NLP and LLM models), Data Science and Machine Learning Intern at BrainyBeam Info-Tech (Car recommendation system, ML models). 
   #Projects: Invoice Data Extraction (OCR, NLP, Django), Stock Price Prediction (LSTM, Streamlit). 
   #Skills: Python, Java, SQL, HTML, CSS, JavaScript, Pandas, NumPy, Matplotlib, Seaborn, MySQL, etc. 
   #Education: B.Tech in AI and Data Science from A D Patel Institute of Technology.
   #Certifications: Duke University, IBM.
#""
#RESUME_CONTEXT = """
#        Diya Shah
#        Contact: +918128426803, Shahdia2630@gmail.com, LinkedIn: Diya Shah
#        Summary: AI developer skilled in machine learning, deep learning, and NLP. Experienced in building chatbots and recommendation systems using LSTM and Random Forest. Proficient in Python, TensorFlow, data preprocessing, model deployment, and performance optimization for actionable insights.,
#        Technical Skills:
#        Programming Languages: Python, Java, SQL, HTML, CSS, JavaScript,
#        Tools: VS Code, PyCharm, GitHub, Jupyter Notebook, Google Colab, PowerBI, Excel,
#        Soft Skills: Communication, Time Management, Presentation, Leadership ,
#        Experience:
#        Data Science Intern, Tech Elecon Pvt. Ltd., Anand, Gujarat (Dec 2024–May 2025): Developed AI-powered HRMS chatbot, integrated NLP and LLM models, improved response time by 60% and reduced HR workload by 40%. Tech: Python, NLP, Machine Learning, MySQL.
#        Data Science and Machine Learning Intern, BrainyBeam Info-Tech, Ahmedabad, Gujarat (May 2024–Jun 2024): Built Car4u, a car recommendation system using Random Forest and XGBoost for personalized recommendations. Tech: Pandas, NumPy, Matplotlib, Seaborn.
#        Projects:
#        Invoice Data Extraction (Python, YOLOv8, OCR-Tesseract, Django): Automated invoice data extraction with OCR and NLP, improved accuracy, reduced processing time by 60%, integrated with accounting software.
#        Stock Price Prediction (Python, LSTM, Streamlit): Developed LSTM-based stock price prediction model with sentiment analysis, built interactive dashboard for real-time analysis.
#        Education: B.Tech in Artificial Intelligence and Data Science, A.D. Patel Institute of Technology (2021–2025), CPI: 8.07.
#        Certifications: Introduction to Machine Learning (Duke University), IBM Data Science Professional Certificate.
#        """
def ask_groq(question, resume_context):
    client = Groq(
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content":  f"""
                    You are Grok, a resume chatbot designed to answer questions ONLY from the uploaded resume content.

                    Rules:
                    - Only use the given resume content.
                    - Do NOT answer any general knowledge, legal, health, political, or personal questions.
                    - If a question is outside the resume, respond with: "Sorry, I am unable to answer this question. I can answer about the resume-related questions only."
                    - Do NOT use any external knowledge or assumptions.Only use the resume content.
                    - If the question is not related to the resume, respond with: "Sorry, I am unable to answer this question. I can answer about the resume-related questions only."
                    - If the question is about the resume, provide a concise and relevant answer based on the resume content.


                    📄 RESUME CONTEXT:
                    {resume_context}
                """
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content

#if __name__ == "__main__":
#    print("Hey!! I am Grok, your assistant. Ask me anything about Diya Shah's resume! (type 'exit' to quit)")
#    while True:
#        user_input = input("You: ")
#        if user_input.lower() == "exit":
#           break
#       answer = ask_groq(user_input)
#        print("Bot:", answer)

if __name__ == "__main__":
    pdf_path = "resume.pdf"  # Replace with the path to your resume PDF file
    resume_context = extract_text_from_pdf(pdf_path)

    print("📄 Resume successfully parsed.")
    print("🤖 Hi! I'm Grok. Ask me anything about the uploaded resume. Type 'exit' to quit.")

    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            break
        response = ask_groq(question, resume_context)
        print("Grok:", response)

        