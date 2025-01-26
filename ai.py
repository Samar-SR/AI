from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()

gorq =  os.getenv("gorq")

def aidata():
    model = ChatGroq(model="llama3-8b-8192", api_key=gorq)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return model,embeddings


