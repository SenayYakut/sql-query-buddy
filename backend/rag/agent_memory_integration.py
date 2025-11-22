"""
Integration with Agent Memory Server for short-term and long-term memory.
"""
from agent_memory_client import MemoryAPIClient
import json
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class AgentMemoryManager:
    """
    Manages memory using Agent Memory Server.
    
    Features:
    - Short-term: Recent conversation context
    - Long-term: Semantic memory with embeddings
    - Entity memory: User preferences and facts
    """
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.memory_client = MemoryAPIClient(base_url=base_url)
        self.llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        
    async def store_interaction(
        self, 
        question: str, 
        sql: str, 
        results: List[Dict],
        insights: str,
        session_id: str,
        user_id: str
    ):
        """
        Store interaction in agent memory server.
        """
        # Create rich memory content
        memory_content = f"""
User Question: {question}
SQL Generated: {sql}
Results Count: {len(results)} rows
Key Insights: {insights[:200]}
"""
        
        # Use LLM to decide what to remember
        messages = [
            {
                "role": "system",
                "content": "You are a memory assistant. Store important information from conversations."
            },
            {
                "role": "user",
                "content": f"Store this SQL query interaction: {memory_content}"
            }
        ]
        
        # Get memory tools
        memory_tools = MemoryAPIClient.get_all_memory_tool_schemas()
        
        # Let LLM decide what to store
        response = await self.llm.apredict_messages(
            messages=messages,
            functions=memory_tools
        )
        
        # Process tool calls
        if hasattr(response, 'additional_kwargs') and response.additional_kwargs.get('function_call'):
            function_call = response.additional_kwargs['function_call']
            
            result = await self.memory_client.resolve_function_call(
                function_name=function_call['name'],
                args=json.loads(function_call['arguments']),
                session_id=session_id,
                user_id=user_id
            )
            
            return result
        
        return None
    
    async def retrieve_relevant_context(
        self,
        question: str,
        session_id: str,
        user_id: str
    ) -> str:
        """
        Retrieve relevant context from memory for the current question.
        """
        # Create messages to trigger memory retrieval
        messages = [
            {
                "role": "system",
                "content": "You are a SQL query assistant with memory. Retrieve relevant past context."
            },
            {
                "role": "user",
                "content": f"I need context for this question: {question}"
            }
        ]
        
        # Get memory tools
        memory_tools = MemoryAPIClient.get_all_memory_tool_schemas()
        
        # Ask LLM to retrieve relevant memories
        response = await self.llm.apredict_messages(
            messages=messages,
            functions=memory_tools
        )
        
        # Process memory retrieval
        if hasattr(response, 'additional_kwargs') and response.additional_kwargs.get('function_call'):
            function_call = response.additional_kwargs['function_call']
            
            result = await self.memory_client.resolve_function_call(
                function_name=function_call['name'],
                args=json.loads(function_call['arguments']),
                session_id=session_id,
                user_id=user_id
            )
            
            # Format the retrieved memories
            if isinstance(result, list):
                return "\n".join([f"- {mem}" for mem in result])
            elif isinstance(result, dict):
                return json.dumps(result, indent=2)
            else:
                return str(result)
        
        return ""
    
    async def get_conversation_context(
        self,
        session_id: str,
        user_id: str,
        limit: int = 5
    ) -> str:
        """
        Get recent conversation history (short-term memory).
        """
        try:
            # Retrieve recent interactions
            history = await self.memory_client.get_conversation_history(
                session_id=session_id,
                user_id=user_id,
                limit=limit
            )
            
            if not history:
                return ""
            
            context_parts = []
            for entry in history:
                context_parts.append(
                    f"Q: {entry.get('question', '')}\n"
                    f"SQL: {entry.get('sql', '')}\n"
                    f"Summary: {entry.get('summary', '')}"
                )
            
            return "\n\n".join(context_parts)
        except Exception as e:
            print(f"Error retrieving conversation context: {e}")
            return ""