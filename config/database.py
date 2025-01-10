from langchain_pinecone import PineconeVectorStore
from .llm import embeddings
import os

API_PINCONE_KEY = os.getenv("PIPE_CONE")
index = "recruit"
vector_store = PineconeVectorStore(
    index_name=index, embedding=embeddings, pinecone_api_key=API_PINCONE_KEY
)
