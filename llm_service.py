import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Initialization
load_dotenv()
INDEX_NAME = "recipe-index" # Your Pinecone index name

# Check for necessary API keys from environment variables
if not os.environ.get("PINECONE_API_KEY"):
    raise ValueError("PINECONE_API_KEY is not set in environment variables.")
if not os.environ.get("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is not set in environment variables.")
if not os.environ.get("HUGGING_FACE_TOKEN"):
    raise ValueError("HUGGING_FACE_TOKEN is not set in environment variables.")

# 2. Initialize the Embedding Model via API
# This now uses the corrected class name for the Hugging Face API.
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-roberta-large-v1",
    huggingfacehub_api_token=os.environ.get("HUGGING_FACE_TOKEN"),
)

# 3. Initialize the Groq LLM
llm = ChatGroq(model="llama-3.1-8b-instant")

# 4. Connect to Your Existing Pinecone Index and Create a Retriever
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=INDEX_NAME, 
    embedding=embeddings
)
retriever = vectorstore.as_retriever()

# 5. Create the RAG Prompt Template
template = """
You are an expert recipe assistant. Use the following retrieved recipes as context to answer the user's question.
Generate the number of recipes requested by the user.

For each recipe, you MUST provide the following information, each on a new line:
- Start with 'Title: ' followed by a creative and descriptive title.
- Then, 'Difficulty: ' (easy, medium, or hard).
- Then, 'Cooking time: ' (in minutes or a range, e.g., 25-30 minutes).
- Then, provide detailed instructions, nutritional information, and substitution suggestions.

Context from retrieved recipes:
{context}

User's Question:
{question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

# 6. Build the RAG Chain
rag_chain = (
    RunnableParallel(
        context=(retriever),
        question=RunnablePassthrough(),
    )
    | prompt
    | llm
    | StrOutputParser()
)

def generate_recipes(query: str) -> str:
    """
    Queries the RAG chain to generate recipes based on user input.
    """
    print(f"Executing RAG query: {query}")
    return rag_chain.invoke(query)

