import os
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

INDEX_NAME = "resume-rag-index1"
EMBEDDING_MODEL = "multilingual-e5-large"
DIMENSIONS = 1024
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 50
REGION = "us-east-1"

class RAGPipeline:
    def __init__(self):
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY", "pcsk_5nN9y_8B7dMTvgKtrLu1r2Mfpfaiiqd28cP1LtAubBebNi6uwKFhXbL8dqCJ1JHfELUWS")
        self.index_name = INDEX_NAME
        self.region = REGION
        self.embeddings = PineconeEmbeddings(model=EMBEDDING_MODEL, dimension=DIMENSIONS, api_key=self.pinecone_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )
        self._init_pinecone()
        self._init_vectorstore()

    def _init_pinecone(self):
        self.pc = Pinecone(api_key=self.pinecone_api_key)


    def _init_vectorstore(self):
        try:
            index = self.pc.Index(self.index_name)
            self.vectorstore = PineconeVectorStore(index, self.embeddings)
        except Exception as e:
            print("Failed to initialize Pinecone vectorstore:", str(e))
            self.vectorstore = None

    def upsert_resume(self, resume_text):
        if not self.vectorstore:
            return
        chunks = self.text_splitter.split_text(resume_text)
        self.vectorstore.add_texts(
            chunks, metadatas=[{"source": "resume_chunk"}] * len(chunks)
        )

    def retrieve_context(self, query, k=3):
        if not self.vectorstore:
            return ""
        docs = self.vectorstore.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in docs])

    def clear_index(self):
        if self.vectorstore:
            self.vectorstore.delete(delete_all=True)
            print(f"Cleared index: {self.index_name}")

# Singleton instance
rag_pipeline = None 

def get_rag_pipeline():
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline
    