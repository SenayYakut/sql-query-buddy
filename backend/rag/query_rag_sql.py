import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Paths
VECTOR_DIR = "backend/rag/vectorstore"
DB_PATH = "backend/db/retail.db"

def format_docs(docs):
    """Format retrieved documents into a single string."""
    return "\n\n".join([f"Table: {doc.metadata.get('table', 'Unknown')}\n{doc.page_content}" for doc in docs])

def generate_sql_for_question(question: str) -> str:
    """
    Generate SQL query using RAG based on the user's question.
    """
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Connect to Chroma vector store
    db = Chroma(
        collection_name="schema_embeddings",
        embedding_function=embeddings,
        persist_directory=VECTOR_DIR
    )

    # Create a retriever (get top 3 most relevant tables)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Initialize ChatOpenAI LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Create prompt template
    template = """You are a SQL expert. Based on the following database schema, generate a SQL query to answer the user's question.

Database Schema:
{context}

User Question: {question}

Important rules:
1. Generate ONLY the SQL query without any explanation, markdown formatting, or code blocks
2. Do not include "```sql" or "```" or any other formatting
3. The query should be syntactically correct SQLite SQL
4. Return just the raw SQL query text

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
    sql_query = rag_chain.invoke(question)
    
    # Clean up the SQL query (remove any markdown formatting if present)
    sql_query = sql_query.strip()
    if sql_query.startswith("```sql"):
        sql_query = sql_query[6:]
    if sql_query.startswith("```"):
        sql_query = sql_query[3:]
    if sql_query.endswith("```"):
        sql_query = sql_query[:-3]
    sql_query = sql_query.strip()
    
    return sql_query

def execute_sql(sql_query: str, db_path: str = DB_PATH):
    """Executes the SQL query against the SQLite database and returns results."""
    print(f"\n🧾 Executing SQL:\n{sql_query}\n")
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return None
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        results = [dict(zip(columns, row)) for row in rows]
        return results
    except sqlite3.Error as e:
        print(f"❌ SQL Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def query_database(user_question: str):
    """Generates SQL using RAG and executes it."""
    print(f"\n{'='*60}")
    print(f"💡 Question: {user_question}")
    print(f"{'='*60}")
    
    # Step 1: Generate SQL using RAG
    print("\n🔍 Generating SQL query using RAG...")
    sql_query = generate_sql_for_question(user_question)
    
    # Step 2: Execute the SQL
    results = execute_sql(sql_query)
    
    return results

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 RAG-Powered SQL Query Executor")
    print("="*60)
    print("\nThis tool uses AI to convert your questions into SQL queries")
    print("and executes them against your database.\n")
    
    # Example queries for testing
    print("Example questions you can ask:")
    print("  • Show all customers")
    print("  • List all products with prices above 50")
    print("  • How many orders were placed last month?")
    print("  • Which customer has spent the most money?")
    print("  • Show me the top 5 best-selling products\n")
    
    while True:
        user_question = input("💡 Ask a question (or 'exit' to quit): ").strip()
        
        if not user_question:
            continue
            
        if user_question.lower() in ["exit", "quit", "q"]:
            print("\n👋 Goodbye!")
            break
        
        output = query_database(user_question)
        
        if output is not None:
            if len(output) == 0:
                print("\n📭 No results found.")
            else:
                print(f"\n✅ Query Results ({len(output)} rows):")
                print("="*60)
                for i, row in enumerate(output, 1):
                    print(f"\nRow {i}:")
                    for key, value in row.items():
                        print(f"  {key}: {value}")
                print("="*60)
        else:
            print("\n❌ Error executing the query. Please try rephrasing your question.")
        
        print()  # Add spacing between queries
# Alias FastAPI expects
def run_rag_query(question: str):
    return query_database(question)
        