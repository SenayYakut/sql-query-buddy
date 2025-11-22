"""
Memory management using Mem0 for intelligent conversation memory.
"""
from mem0 import Memory
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Mem0MemoryManager:
    """
    Manages conversation memory using Mem0.
    
    Features:
    - Automatic memory extraction from conversations
    - Semantic search across past interactions
    - Smart context retrieval
    """
    
    def __init__(self):
        # Configure Mem0 with Qdrant (included in mem0ai)
        config = {
            "version": "v1.1",
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0,
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "sql_buddy_memory",
                    "path": "./qdrant_storage",
                }
            },
        }
        
        self.memory = Memory.from_config(config)
    
    def add_interaction(
        self, 
        question: str, 
        sql: str, 
        results: List[Dict],
        insights: str,
        user_id: str,
        session_id: str
    ):
        """
        Add interaction to memory. Mem0 will automatically extract
        and store important information.
        """
        # Create rich conversation message
        message = f"""User asked: "{question}"

Generated SQL query: {sql}

Query returned {len(results)} rows.

Key insights: {insights[:300]}

This interaction happened in session {session_id}."""
        
        # Mem0 automatically extracts and stores relevant memories
        result = self.memory.add(
            messages=[{"role": "user", "content": message}],
            user_id=user_id,
            metadata={
                "session_id": session_id,
                "question": question,
                "type": "sql_query"
            }
        )
        
        return result
    
    def get_relevant_memories(
        self, 
        question: str, 
        user_id: str,
        limit: int = 3
    ) -> str:
        """
        Search for relevant past memories based on the current question.
        """
        # Mem0 uses semantic search to find relevant memories
        memories = self.memory.search(
            query=question,
            user_id=user_id,
            limit=limit
        )
        
        if not memories or len(memories) == 0:
            return ""
        
        # Format memories as context
        context_parts = ["RELEVANT PAST CONTEXT:"]
        for mem in memories:
            memory_text = mem.get('memory', mem.get('text', ''))
            if memory_text:
                context_parts.append(f"• {memory_text}")
        
        return "\n".join(context_parts)
    
    def get_all_memories(self, user_id: str) -> List[Dict]:
        """Get all memories for a user."""
        try:
            return self.memory.get_all(user_id=user_id)
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def delete_memory(self, memory_id: str):
        """Delete a specific memory."""
        try:
            self.memory.delete(memory_id=memory_id)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_all_memories(self, user_id: str):
        """Delete all memories for a user."""
        try:
            self.memory.delete_all(user_id=user_id)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}