import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from groq import Groq
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# API Keys and Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set this in your .env file!
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  # Set this in your .env file!
INDEX_NAME = "resume-rag-index"
MODEL_NAME = "multilingual-e5-large"  # Pinecone Embeddings model
DIMENSIONS = 1024
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Initialize clients
client = Groq(api_key=GROQ_API_KEY)
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index = pinecone.Index(INDEX_NAME)
embeddings = PineconeEmbeddings(model=MODEL_NAME, dimension=DIMENSIONS, api_key=PINECONE_API_KEY)
vectorstore = PineconeVectorStore(index, embeddings)

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def chunk_text(text):
    """Splits text into chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_text(text)

def process_inbuilt_pdf_and_upsert():
    """Reads, chunks, embeds, and upserts resume PDF to Pinecone."""
    pdf_path = "C:/Users/diyas/Desktop/Prompt Engineering/CHATBOT/RAG and Pinecone/Diya_Resume_Data Analyst.pdf"
    try:
        text = extract_text_from_pdf(pdf_path)
        if not text:
            print("No text extracted from PDF.")
            return
        chunks = chunk_text(text)
        if not chunks:
            print("No text chunks to upsert.")
            return
        # Upsert using LangChain's PineconeVectorStore (handles embedding)
        vectorstore.add_texts(chunks)
        print(f"Resume upserted to Pinecone index. Total chunks: {len(chunks)}")
    except Exception as e:
        print(f"Error processing PDF: {e}")

def retrieve_context(query, k=3):
    """Retrieves top-k relevant chunks from Pinecone using embeddings."""
    try:
        docs = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return []

def main():
    while True:
        print("\nMenu:")
        print("1. Upsert resume PDF")
        print("2. Quit")
        choice = input("Select an option (1/2): ").strip()
        if choice == "1":
            pdf_path = input("Enter path to resume PDF (or press Enter for default): ").strip()
            if not pdf_path:
                pdf_path = "C:/Users/diyas/Desktop/Prompt Engineering/CHATBOT/RAG and Pinecone/Diya_Resume_Data Analyst.pdf"
            process_inbuilt_pdf_and_upsert()
        elif choice == "2":
            print("Exiting.")
            break
        else:
            print("Invalid option. Please select 1 or 2.")

if __name__ == "__main__":
    main()