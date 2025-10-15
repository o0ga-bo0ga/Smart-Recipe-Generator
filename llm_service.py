from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import pickle

load_dotenv()

# Load index from .pkl (once)
with open('./data/index.pkl', 'rb') as f:
    index = pickle.load(f)

# Groq LLM
groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.environ["GROQ_API_KEY"]
)

def generate_recipes(query):
    return index.query(query, llm=groq_llm)