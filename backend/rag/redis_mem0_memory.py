"""
Hybrid memory system using Redis + Mem0:
- Redis: Fast short-term conversation memory (last 10 exchanges)
- Mem0/Qdrant: Long-term semantic memory (full history, searchable)
"""
import redis
import json
from typing import List, Dict, Optional
from datetime import datetime
from mem0 import Memory
import os
from dotenv import load_dotenv

load_dotenv()

class HybridMemoryManager:
    """
    Two-tier intelligent memory system.
    
    Tier 1 (Redis): 
    - Fast access to recent conversation
    - Key-value storage with TTL
    - Session-based memory
    
    Tier 2 (Mem0/Qdrant):
    - Semantic search across all history
    - Automatic memory extraction
    - Persistent long-term storage
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Initialize Redis for short-term memory
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Test Redis connection
        try:
            self.redis_client.ping()
            print("✅ Redis connected successfully")
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            print("Make sure Redis is running: redis-server")
        
        # Initialize Mem0 for long-term memory
        mem0_config = {
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
        
        self.mem0 = Memory.from_config(mem0_config)
        print("✅ Mem0 initialized successfully")
    
    # ==================== SHORT-TERM MEMORY (Redis) ====================
    
    def add_to_short_term(self, session_id: str, interaction: Dict):
        """
        Store recent conversation in Redis.
        Fast access, expires after 1 hour.
        """
        try:
            key = f"conversation:{session_id}"
            
            # Add timestamp
            interaction['timestamp'] = datetime.now().isoformat()
            
            # Push to Redis list (newest first)
            self.redis_client.lpush(key, json.dumps(interaction))
            
            # Keep only last 10 interactions
            self.redis_client.ltrim(key, 0, 9)
            
            # Set expiration (1 hour)
            self.redis_client.expire(key, 3600)
            
            print(f"📝 Stored in Redis: {interaction['question'][:50]}...")
            
        except Exception as e:
            print(f"Error storing in Redis: {e}")
    
    def get_short_term_context(self, session_id: str, limit: int = 3) -> str:
        """
        Get recent conversation from Redis for immediate context.
        """
        try:
            key = f"conversation:{session_id}"
            items = self.redis_client.lrange(key, 0, limit - 1)
            
            if not items:
                return ""
            
            context_parts = ["RECENT CONVERSATION (from Redis):"]
            for item in reversed(items):  # Chronological order
                data = json.loads(item)
                context_parts.append(
                    f"Q: {data['question']}\n"
                    f"SQL: {data['sql']}\n"
                    f"Results: {data.get('result_summary', 'N/A')}"
                )
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            print(f"Error retrieving from Redis: {e}")
            return ""
    
    def clear_short_term(self, session_id: str):
        """Clear Redis conversation for a session."""
        try:
            key = f"conversation:{session_id}"
            self.redis_client.delete(key)
            return {"status": "success", "message": f"Cleared Redis memory for {session_id}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ==================== LONG-TERM MEMORY (Mem0/Qdrant) ====================
    
    def add_to_long_term(
        self, 
        question: str, 
        sql: str, 
        results: List[Dict],
        insights: str,
        user_id: str,
        session_id: str
    ):
        """
        Store important interactions in Mem0 for semantic search.
        Mem0 automatically extracts relevant information.
        """
        try:
            # Create rich conversation message
            message = f"""User asked: "{question}"

Generated SQL query: {sql}

Query returned {len(results)} rows.

Key insights: {insights[:300]}

This interaction happened in session {session_id}."""
            
            # Mem0 automatically extracts and stores memories
            result = self.mem0.add(
                messages=[{"role": "user", "content": message}],
                user_id=user_id,
                metadata={
                    "session_id": session_id,
                    "question": question,
                    "type": "sql_query"
                }
            )
            
            print(f"💾 Stored in Mem0: {question[:50]}...")
            return result
            
        except Exception as e:
            print(f"Error storing in Mem0: {e}")
            return None
    
    def search_long_term(self, question: str, user_id: str, limit: int = 2) -> str:
        """
        Search long-term memory using semantic search.
        """
        try:
            memories = self.mem0.search(
                query=question,
                user_id=user_id,
                limit=limit
            )
            
            if not memories or len(memories) == 0:
                return ""
            
            context_parts = ["RELEVANT PAST CONTEXT (from Mem0):"]
            for mem in memories:
                # Fix: Handle both dict and string responses
                if isinstance(mem, dict):
                    memory_text = mem.get('memory', mem.get('text', ''))
                elif isinstance(mem, str):
                    memory_text = mem
                else:
                    memory_text = str(mem)
                
                if memory_text:
                    context_parts.append(f"• {memory_text}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            print(f"Error searching Mem0: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    # ==================== COMBINED CONTEXT ====================
    
    def get_combined_context(
        self, 
        question: str, 
        session_id: str, 
        user_id: str
    ) -> Dict[str, str]:
        """
        Get both short-term (Redis) and long-term (Mem0) context.
        
        Returns:
            {
                "short_term": "Recent conversation from Redis",
                "long_term": "Relevant memories from Mem0",
                "combined": "Both merged"
            }
        """
        # Get short-term from Redis
        short_term = self.get_short_term_context(session_id, limit=3)
        
        # Get long-term from Mem0
        long_term = self.search_long_term(question, user_id, limit=2)
        
        # Combine
        combined = []
        if short_term:
            combined.append(short_term)
        if long_term:
            combined.append(long_term)
        
        combined_text = "\n\n".join(combined) if combined else "No relevant context found."
        
        return {
            "short_term": short_term or "No recent conversation",
            "long_term": long_term or "No relevant past context",
            "combined": combined_text
        }
    
    # ==================== FULL INTERACTION STORAGE ====================
    
    def store_interaction(
        self,
        question: str,
        sql: str,
        results: List[Dict],
        insights: str,
        user_id: str,
        session_id: str
    ):
        """
        Store interaction in BOTH Redis (short-term) and Mem0 (long-term).
        """
        # Prepare interaction data
        interaction = {
            "question": question,
            "sql": sql,
            "result_count": len(results),
            "result_summary": f"{len(results)} rows returned",
            "insights_preview": insights[:100]
        }
        
        # Store in Redis (fast, recent)
        self.add_to_short_term(session_id, interaction)
        
        # Store in Mem0 (semantic, permanent)
        self.add_to_long_term(
            question=question,
            sql=sql,
            results=results,
            insights=insights,
            user_id=user_id,
            session_id=session_id
        )
    
    # ==================== MEMORY MANAGEMENT ====================
    
    def get_all_memories(self, user_id: str) -> List[Dict]:
        """Get all long-term memories from Mem0."""
        try:
            return self.mem0.get_all(user_id=user_id)
        except Exception as e:
            print(f"Error retrieving all memories: {e}")
            return []
    
    def delete_all_memories(self, user_id: str):
        """Delete all memories for a user from Mem0."""
        try:
            self.mem0.delete_all(user_id=user_id)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_memory_stats(self, session_id: str, user_id: str) -> Dict:
        """Get statistics about stored memories."""
        try:
            # Redis stats
            redis_key = f"conversation:{session_id}"
            redis_count = self.redis_client.llen(redis_key)
            redis_ttl = self.redis_client.ttl(redis_key)
            
            # Mem0 stats
            mem0_memories = self.get_all_memories(user_id)
            mem0_count = len(mem0_memories) if mem0_memories else 0
            
            return {
                "redis": {
                    "recent_exchanges": redis_count,
                    "expires_in_seconds": redis_ttl if redis_ttl > 0 else 0
                },
                "mem0": {
                    "total_memories": mem0_count
                },
                "total": redis_count + mem0_count
            }
        except Exception as e:
            return {"error": str(e)}