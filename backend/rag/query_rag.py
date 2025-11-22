from dotenv import load_dotenv
import os

load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

VECTOR_DIR = "backend/rag/vectorstore"

def format_docs(docs):
    """Format retrieved documents into a single string."""
    return "\n\n".join([f"Table: {doc.metadata.get('table', 'Unknown')}\n{doc.page_content}" for doc in docs])

def run_rag_query(question: str):
    """
    Run a RAG query using the schema embeddings to generate SQL.
    """
    print(f"\n{'='*60}")
    print(f"💡 User Question: {question}")
    print(f"{'='*60}")
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Connect to Chroma vector store
    db = Chroma(
        collection_name="schema_embeddings",
        embedding_function=embeddings,
        persist_directory=VECTOR_DIR
    )

    # Create a retriever (get top 2 most relevant tables)
    retriever = db.as_retriever(search_kwargs={"k": 2})

    # Initialize ChatOpenAI LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Create prompt template
    template = """You are a SQL expert. Based on the following database schema, generate a SQL query to answer the user's question.

Database Schema:
{context}

User Question: {question}

Generate ONLY the SQL query without any explanation. The query should be syntactically correct SQLite SQL.

SQL Query:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Create RAG chain using LCEL (LangChain Expression Language)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Run the query
    result = rag_chain.invoke(question)
    
    # Also get the source documents to show which tables were used
    relevant_docs = retriever.invoke(question)
    
    print(f"\n📊 Relevant Tables Found:")
    for doc in relevant_docs:
        print(f"  • {doc.metadata.get('table', 'Unknown')}")
    
    print(f"\n📝 Generated SQL Query:")
    print(f"{result}")
    print(f"{'='*60}\n")
    
    return result

def run_rag_with_explanation(question: str):
    """
    Run RAG query with detailed explanation.
    """
    print(f"\n{'='*60}")
    print(f"💡 User Question: {question}")
    print(f"{'='*60}")
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Connect to Chroma vector store
    db = Chroma(
        collection_name="schema_embeddings",
        embedding_function=embeddings,
        persist_directory=VECTOR_DIR
    )

    # Create a retriever
    retriever = db.as_retriever(search_kwargs={"k": 2})

    # Initialize ChatOpenAI LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Create prompt template with explanation
    template = """You are a helpful SQL expert assistant. Based on the following database schema, help the user with their question.

Database Schema:
{context}

User Question: {question}

Provide:
1. A brief explanation of which tables are needed
2. The SQL query
3. A brief explanation of what the query does

Response:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Create RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Run the query
    result = rag_chain.invoke(question)
    
    # Get source documents
    relevant_docs = retriever.invoke(question)
    
    print(f"\n📊 Relevant Tables Found:")
    for doc in relevant_docs:
        print(f"  • {doc.metadata.get('table', 'Unknown')}")
    
    print(f"\n💬 AI Response:")
    print(result)
    print(f"{'='*60}\n")
    
    return result

if __name__ == "__main__":
    print("\n🚀 Testing RAG-based SQL Query Generation\n")
    
    # Test 1: Simple queries
    print("="*60)
    print("TEST 1: Simple SQL Generation (No Explanation)")
    print("="*60)
    
    simple_questions = [
        "Show all customers",
        "List all products with their prices",
        "Find all orders from the last month",
    ]

    for q in simple_questions:
        run_rag_query(q)

    # Test 2: Queries with explanation
    print("\n" + "="*60)
    print("TEST 2: SQL Generation with Explanation")
    print("="*60)
    
    complex_questions = [
        "Which customers have placed the most orders?",
        "What is the total revenue by product category?",
    ]

    for q in complex_questions:
        run_rag_with_explanation(q)