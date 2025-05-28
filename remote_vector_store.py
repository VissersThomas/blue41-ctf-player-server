import logging
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_milvus import Milvus

# Load environment variables
load_dotenv()


def connect_to_remote_vector_db(embeddings=None):
    """Connect to existing, pre-populated Milvus vector database"""

    # Get configuration from environment variables
    MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
    MILVUS_USER = os.getenv("MILVUS_USER")
    MILVUS_PASSWORD = os.getenv("MILVUS_PASSWORD")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")

    # Select embeddings (must match what was used to populate the DB)
    if not embeddings:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")

    # Build connection args
    connection_args = {
        "host": MILVUS_HOST,
        "port": MILVUS_PORT,
        "user": MILVUS_USER,
        "password": MILVUS_PASSWORD
    }

    print(f"Connecting to existing Milvus collection '{COLLECTION_NAME}' at {MILVUS_HOST}:{MILVUS_PORT}")

    # Connect to existing Milvus collection
    db = Milvus(
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        connection_args=connection_args,
        drop_old=False  # Don't drop existing data
    )

    print("Successfully connected to pre-populated Milvus database")
    return db