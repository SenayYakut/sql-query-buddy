from dotenv import load_dotenv
import os

load_dotenv()

import sqlite3
from typing import List, Dict

# Updated imports for new LangChain structure
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

SCHEMA_FILE = "backend/db/schema.sql"
VECTOR_DIR = "backend/rag/vectorstore"

def load_schema():
    """Reads the schema.sql file and returns the full text."""
    print("📥 Loading schema.sql...")
    with open(SCHEMA_FILE, "r") as f:
        return f.read()

def split_schema_into_chunks(schema_text):
    """
    Splits schema.sql into chunks per table.
    Each CREATE TABLE statement becomes one document.
    """
    print("🔪 Splitting schema into table chunks...")
    chunks = []
    statements = schema_text.split("CREATE TABLE")

    for s in statements:
        if "(" in s:
            table_name = s.split("(")[0].strip()
            chunk = "CREATE TABLE " + s
            chunks.append({"table": table_name, "text": chunk})

    print(f"📄 Found {len(chunks)} tables to embed.")
    return chunks

def embed_schema():
    """
    Embeds each table definition into a Chroma vector DB.
    """
    print("🧠 Embedding schema into vector database...")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    db = Chroma(
        collection_name="schema_embeddings",
        embedding_function=embeddings,
        persist_directory=VECTOR_DIR
    )

    # Clear old vectors
    db.delete_collection()
    db = Chroma(
        collection_name="schema_embeddings",
        embedding_function=embeddings,
        persist_directory=VECTOR_DIR
    )

    schema_text = load_schema()
    chunks = split_schema_into_chunks(schema_text)

    for c in chunks:
        db.add_texts(
            texts=[c["text"]],
            metadatas=[{"table": c["table"]}]
        )
        print(f"✅ Embedded table: {c['table']}")

    # Note: persist() is no longer needed in newer versions of Chroma
    # The data is automatically persisted when persist_directory is set
    print("🎉 All schema embeddings stored successfully!")

if __name__ == "__main__":
    print("▶ Running embed_schema.py")
    embed_schema()
    print("▶ Done!")