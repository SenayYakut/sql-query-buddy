from langgraph import Graph
from .llm_agent import LLMWrapper
from .schema_retriever import SchemaRetriever
import sqlite3

class SQLQueryAgent:
    def __init__(self, db_path="db/retail.db"):
        self.llm = LLMWrapper()
        self.retriever = SchemaRetriever()
        self.db_path = db_path

    def execute_sql(self, sql: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        try:
            cur.execute(sql)
            results = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []
        except Exception as e:
            results, columns = [], []
            print(f"SQL Execution Error: {e}")
        conn.close()
        return results, columns

    def run(self, user_query: str):
        # Step 1: Retrieve schema context
        context_docs = self.retriever.retrieve(user_query)
        context_text = "\n".join([doc.page_content for doc in context_docs])

        # Step 2: Generate SQL
        prompt_sql = f"""
        You are a SQL expert. Given the database schema context below:
        {context_text}

        Generate a valid SQL query for this user request:
        {user_query}
        """
        sql = self.llm.run(prompt_sql)

        # Step 3: Execute SQL
        results, columns = self.execute_sql(sql)

        # Step 4: Generate AI insights
        prompt_insights = f"""
        Given the SQL results: {results}
        Provide a short, actionable summary and insights.
        """
        insights = self.llm.run(prompt_insights)

        return {"sql": sql, "results": results, "columns": columns, "insights": insights}
