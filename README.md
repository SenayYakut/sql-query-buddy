# 🤖 SQL Query Buddy

**AI-Powered Conversational Database Assistant with Hybrid Memory System**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-7.0-DC382D.svg)](https://redis.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://www.langchain.com/)

Transform natural language questions into SQL queries with AI-powered insights, conversation memory, and intelligent optimization suggestions.

---

## 🌟 Features

### Core Capabilities
- 🧠 **RAG-Powered SQL Generation** - Semantic schema retrieval using ChromaDB vector database
- 💬 **Hybrid Memory System** - Redis for short-term + Mem0/Qdrant for long-term semantic memory
- 🔄 **Conversation Context** - Understands follow-up questions like "filter them to California"
- 📊 **AI-Driven Insights** - GPT-4 powered data analysis and business recommendations
- ⚡ **Query Optimization** - Automatic performance suggestions and indexing recommendations
- 📖 **Beginner-Friendly Explanations** - Plain English SQL explanations
- 🎨 **Modern UI** - Beautiful React interface with real-time results

### Technical Highlights
- **Two-Tier Memory Architecture**: Redis (fast, recent) + Mem0/Qdrant (semantic, permanent)
- **RAG Implementation**: Retrieves only relevant table schemas using semantic search
- **Multi-Step AI Pipeline**: SQL generation → Execution → Analysis → Insights
- **Production-Ready**: Error handling, logging, session management, TTL caching

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend (React)               │
│           Natural Language Interface             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│              FastAPI Backend                     │
│  ┌──────────────────────────────────────────┐  │
│  │   1. Memory Retrieval (Redis + Mem0)     │  │
│  │      • Short-term: Recent conversation   │  │
│  │      • Long-term: Semantic search        │  │
│  └──────────────┬───────────────────────────┘  │
│                 ▼                                │
│  ┌──────────────────────────────────────────┐  │
│  │   2. Schema Retrieval (RAG/ChromaDB)     │  │
│  │      • Semantic search for tables        │  │
│  │      • Top-k relevant schemas            │  │
│  └──────────────┬───────────────────────────┘  │
│                 ▼                                │
│  ┌──────────────────────────────────────────┐  │
│  │   3. SQL Generation (GPT-4 + LangChain)  │  │
│  │      • Context-aware query creation      │  │
│  │      • SQLite syntax optimization        │  │
│  └──────────────┬───────────────────────────┘  │
│                 ▼                                │
│  ┌──────────────────────────────────────────┐  │
│  │   4. Query Execution (SQLite)            │  │
│  │      • Parameterized queries             │  │
│  │      • Performance timing                │  │
│  └──────────────┬───────────────────────────┘  │
│                 ▼                                │
│  ┌──────────────────────────────────────────┐  │
│  │   5. AI Analysis (GPT-4)                 │  │
│  │      • Explanation generation            │  │
│  │      • Optimization suggestions          │  │
│  │      • Business insights                 │  │
│  └──────────────┬───────────────────────────┘  │
│                 ▼                                │
│  ┌──────────────────────────────────────────┐  │
│  │   6. Memory Storage (Redis + Mem0)       │  │
│  │      • Store for future reference        │  │
│  │      • TTL management                    │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration and RAG implementation
- **OpenAI GPT-4** - SQL generation and analysis
- **ChromaDB** - Vector database for schema embeddings
- **Redis** - Fast in-memory short-term conversation cache
- **Mem0** - Intelligent long-term memory with semantic search
- **Qdrant** - Vector database backend for Mem0
- **SQLite** - Sample retail database

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe JavaScript
- **CSS-in-JS** - Styled components

### AI/ML
- **text-embedding-3-large** - Schema embeddings (OpenAI)
- **text-embedding-3-small** - Memory embeddings (OpenAI)
- **gpt-4** - SQL generation and analysis
- **gpt-4o-mini** - Memory extraction

---

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Redis** (via Homebrew or Docker)
- **OpenAI API Key**

---

## 🚀 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/sql-query-buddy.git
cd sql-query-buddy
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
```

### 3. Initialize Vector Databases

```bash
# Embed database schemas into ChromaDB
python backend/rag/embed_schema.py
```

Expected output:
```
📥 Loading schema.sql...
🔪 Splitting schema into table chunks...
📄 Found 4 tables to embed.
✅ Embedded table: customers
✅ Embedded table: products
✅ Embedded table: orders
✅ Embedded table: order_items
🎉 All schema embeddings stored successfully!
```

### 4. Start Redis

```bash
# Using Homebrew (Mac)
brew install redis
redis-server

# Using Docker
docker run -d -p 6379:6379 redis:latest
```

### 5. Start Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs on: **http://localhost:8000**

### 6. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: **http://localhost:3000**

---

## 🎯 Usage Examples

### Basic Query
```
User: "Show me the top 5 customers by total purchase amount"

Response:
✅ SQL: SELECT c.name, SUM(o.total_amount) as total...
✅ Results: 5 rows
✅ Explanation: "This query finds the top 5 customers..."
✅ Insights: "Alice Chen is your top customer with $5,000..."
✅ Optimization: "Consider adding an index on orders.customer_id..."
```

### Follow-up with Context (Memory in Action!)
```
User: "Now filter them to California only"

Response:
✅ SQL: WITH top_customers AS (SELECT...) WHERE region='California'
✅ Understands "them" refers to previous top 5 customers
✅ Uses Redis short-term + Mem0 long-term memory
```

### Complex Multi-Table Query
```
User: "Which product category made the most revenue last month?"

Response:
✅ Automatically retrieves: products, orders, order_items schemas
✅ Generates proper JOIN query
✅ Provides revenue breakdown and trends
```

---

## 🔌 API Endpoints

### Query Endpoint
```http
POST /rag/query
Content-Type: application/json

{
  "question": "Show me the top 5 customers",
  "session_id": "default",
  "user_id": "anonymous"
}
```

**Response:**
```json
{
  "sql": "SELECT ...",
  "results": [...],
  "insights": "Key findings...",
  "explanation": "This query...",
  "optimization": "Performance tips...",
  "execution_time_ms": 15.42,
  "memory_context": {
    "short_term": "Recent conversation...",
    "long_term": "Relevant past context...",
    "combined": "Full context..."
  }
}
```

### Memory Stats
```http
GET /rag/memory/stats?session_id=default&user_id=anonymous
```

**Response:**
```json
{
  "redis": {
    "recent_exchanges": 3,
    "expires_in_seconds": 3421
  },
  "mem0": {
    "total_memories": 5
  },
  "total": 8
}
```

### Clear Session Memory
```http
DELETE /rag/memory/redis/{session_id}
```

### Clear User Long-term Memory
```http
DELETE /rag/memory/mem0/{user_id}
```

### View All Memories
```http
GET /rag/memory/all/{user_id}
```

---

## 📊 Database Schema

The project includes a sample retail database with:

### Tables
- **customers** - Customer information (id, name, email, region)
- **products** - Product catalog (id, name, category, price, stock)
- **orders** - Order records (id, customer_id, order_date, total_amount)
- **order_items** - Order line items (id, order_id, product_id, quantity, price)

### Sample Data
- 10+ customers across different regions
- 15+ products in various categories
- 20+ orders with multiple line items

---

## 🧪 Testing with Postman

### Import Collection

1. Open Postman
2. Click **Import** → **Raw Text**
3. Paste this collection:

```json
{
  "info": {
    "name": "SQL Query Buddy API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Query - Basic",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"question\": \"Show me the top 5 customers by total purchase amount\",\n  \"session_id\": \"test-session\",\n  \"user_id\": \"test-user\"\n}"
        },
        "url": "http://localhost:8000/rag/query"
      }
    },
    {
      "name": "Query - Follow-up",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"question\": \"Now filter them to California only\",\n  \"session_id\": \"test-session\",\n  \"user_id\": \"test-user\"\n}"
        },
        "url": "http://localhost:8000/rag/query"
      }
    },
    {
      "name": "Memory Stats",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/rag/memory/stats?session_id=test-session&user_id=test-user"
      }
    },
    {
      "name": "Get All Memories",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/rag/memory/all/test-user"
      }
    },
    {
      "name": "Clear Redis Memory",
      "request": {
        "method": "DELETE",
        "url": "http://localhost:8000/rag/memory/redis/test-session"
      }
    }
  ]
}
```

### Test Sequence

1. **Test Basic Query** - Run "Query - Basic"
2. **Check Memory** - Run "Memory Stats" (should show 1 exchange)
3. **Test Context Memory** - Run "Query - Follow-up" 
4. **Verify Memory** - Run "Memory Stats" (should show 2 exchanges)
5. **View Memories** - Run "Get All Memories"
6. **Clean Up** - Run "Clear Redis Memory"

---

## 🎨 Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Query Results with AI Insights
![Query Results](screenshots/query-results.png)

### Conversation Memory in Action
![Memory Demo](screenshots/memory-demo.png)

---

## 🧠 How It Works

### 1. Memory System (Redis + Mem0)

**Short-term (Redis):**
- Stores last 10 conversation exchanges per session
- TTL: 1 hour
- Use case: Immediate follow-up questions

**Long-term (Mem0/Qdrant):**
- Semantic memory with automatic extraction
- Persistent storage with vector embeddings
- Use case: Historical patterns, user preferences

### 2. RAG Implementation

```python
# Semantic search for relevant schemas
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Only retrieves top 3 most relevant tables
# Reduces token usage and improves accuracy
```

### 3. SQL Generation Pipeline

```
User Question 
  → Memory Retrieval (Redis + Mem0)
  → Schema Retrieval (ChromaDB RAG)
  → LLM Prompt Construction
  → GPT-4 SQL Generation
  → Query Execution
  → Multi-step Analysis
  → Memory Storage
```

---

## 🔒 Security Considerations

- **API Keys**: Never commit `.env` files
- **SQL Injection**: Uses parameterized queries
- **Input Validation**: Pydantic models validate all inputs
- **Rate Limiting**: Redis-based rate limiting ready
- **Error Handling**: Comprehensive exception handling

---

## 🚧 Future Enhancements

- [ ] Support for multiple database types (PostgreSQL, MySQL)
- [ ] Query history visualization
- [ ] Export results to CSV/Excel
- [ ] Collaborative query sharing
- [ ] Advanced analytics dashboard
- [ ] Natural language to database schema generation
- [ ] Multi-tenant support
- [ ] API authentication (OAuth2/JWT)

---

## 📝 Project Structure

```
sql-query-buddy/
├── backend/
│   ├── db/
│   │   ├── retail.db          # SQLite database
│   │   └── schema.sql         # Database schema
│   ├── rag/
│   │   ├── router.py          # Main API endpoints
│   │   ├── redis_mem0_memory.py  # Hybrid memory manager
│   │   ├── embed_schema.py    # Schema embedding script
│   │   └── vectorstore/       # ChromaDB storage
│   └── main.py               # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── RagQuery.tsx      # Main UI component
│   │   └── App.tsx           # App entry point
│   └── package.json
├── qdrant_storage/           # Mem0 vector database
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-4 and embedding models
- **LangChain** - RAG orchestration framework
- **Redis** - High-performance in-memory database
- **Mem0** - Intelligent memory management
- **ChromaDB** - Vector database for embeddings
- **FastAPI** - Modern Python web framework

---

## 📞 Contact

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## ⭐ Star History

If you find this project helpful, please give it a star! ⭐

---

**Built with ❤️ using AI, RAG, and Modern Web Technologies**
