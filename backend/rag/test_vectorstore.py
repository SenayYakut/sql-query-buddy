from dotenv import load_dotenv
import os

load_dotenv()

# Updated imports for new LangChain structure
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

VECTOR_DIR = "backend/rag/vectorstore"

def test_chroma():
    print("🔍 Testing Chroma vector store...")
    
    # Load embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Connect to the persisted vector store
    db = Chroma(
        collection_name="schema_embeddings",
        embedding_function=embeddings,
        persist_directory=VECTOR_DIR
    )

    # Test 1: Search for tables containing "customer"
    print("\n📋 Test 1: Searching for 'customer'...")
    query = "customer information"
    results = db.similarity_search(query, k=2)  # top 2 closest matches

    for i, r in enumerate(results, 1):
        print(f"\n  Result {i}:")
        print(f"  Table: {r.metadata.get('table', 'Unknown')}")
        print(f"  Text snippet: {r.page_content[:150]}...")

    # Test 2: Search for tables related to "orders"
    print("\n📋 Test 2: Searching for 'orders'...")
    query = "order details and tracking"
    results = db.similarity_search(query, k=2)

    for i, r in enumerate(results, 1):
        print(f"\n  Result {i}:")
        print(f"  Table: {r.metadata.get('table', 'Unknown')}")
        print(f"  Text snippet: {r.page_content[:150]}...")

    # Test 3: Search for tables related to "products"
    print("\n📋 Test 3: Searching for 'product inventory'...")
    query = "product price and stock"
    results = db.similarity_search(query, k=2)

    for i, r in enumerate(results, 1):
        print(f"\n  Result {i}:")
        print(f"  Table: {r.metadata.get('table', 'Unknown')}")
        print(f"  Text snippet: {r.page_content[:150]}...")

    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_chroma()