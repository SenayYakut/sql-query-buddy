# Teacher Testing Guide 🎓

**Student:** Senay Yakut
**Project:** SQL Query Buddy - AI-Powered RAG SQL Assistant
**Live Demo URL:** https://nonconsuming-delly-dagny.ngrok-free.dev/docs

---

## ⚡ Quick Start (3 Minutes)

### Step 1: Open the App
Click this link: **https://nonconsuming-delly-dagny.ngrok-free.dev/docs**

You'll see the FastAPI interactive documentation interface.

### Step 2: Get Your OpenAI API Key
If you don't have one:
1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account (free)
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...` or `sk-...`)

### Step 3: Test the App
1. On the API docs page, find **"POST /rag/query"**
2. Click it to expand
3. Click **"Try it out"** button (top right)
4. Replace the example JSON with:

```json
{
  "question": "Show me the top 5 customers by total purchase amount",
  "session_id": "test-session",
  "user_id": "teacher",
  "api_key": "YOUR_ACTUAL_OPENAI_KEY_HERE"
}
```

5. Click **"Execute"** button
6. Scroll down to see the response!

---

## 📋 What You'll See in the Response

```json
{
  "sql": "SELECT c.name, SUM(o.total_amount) as total_spent...",
  "results": [
    {"name": "Alice Chen", "total_spent": 5000},
    {"name": "Bob Smith", "total_spent": 4500},
    ...
  ],
  "explanation": "This query joins the customers and orders tables...",
  "insights": "Alice Chen is your top customer with $5,000 in purchases...",
  "optimization": "Consider adding an index on orders.customer_id...",
  "execution_time_ms": 15.42,
  "memory_context": {...}
}
```

**What This Shows:**
- ✅ **SQL Query:** AI-generated SQL (using RAG schema retrieval)
- ✅ **Results:** Actual data from the database
- ✅ **Explanation:** Plain English explanation
- ✅ **AI Insights:** Business intelligence from the data
- ✅ **Optimization:** Performance suggestions
- ✅ **Memory Context:** Conversation history (for follow-ups)

---

## 🎯 Test Scenarios

### Test 1: Basic Query
**Question:** `"Show me all products"`

**Expected:**
- Simple SELECT query
- List of products with names, prices, categories
- Explanation of the query

### Test 2: Aggregation
**Question:** `"What's the average product price?"`

**Expected:**
- Uses AVG() SQL function
- Single result with average
- Explanation of aggregation

### Test 3: Complex Join
**Question:** `"Show me orders with customer names"`

**Expected:**
- Properly joins orders and customers tables
- Results show both order details and customer names
- Explanation of the JOIN

### Test 4: Top-N Query
**Question:** `"Show top 5 best-selling products"`

**Expected:**
- Uses ORDER BY and LIMIT
- Aggregates by product
- Ranked results

### Test 5: **Conversation Memory** (Most Important!)

**First Request:**
```json
{
  "question": "Show me the top 5 customers",
  "session_id": "memory-test",
  "user_id": "teacher",
  "api_key": "YOUR_KEY"
}
```

**Second Request (Same session):**
```json
{
  "question": "Now filter them to California only",
  "session_id": "memory-test",
  "user_id": "teacher",
  "api_key": "YOUR_KEY"
}
```

**Expected:**
- Second query understands "them" = top 5 customers from first query
- Adds WHERE region='California' to the previous query
- Shows the hybrid memory system (Redis + Mem0) is working

---

## 🔍 What Makes This Project Special

### 1. RAG (Retrieval-Augmented Generation)
- Uses **ChromaDB** vector database to store database schemas
- Semantically searches for relevant tables based on the question
- Only retrieves needed schema info (efficient!)
- Reduces hallucination by providing actual schema context

### 2. Hybrid Memory System
- **Redis:** Short-term memory (last 10 exchanges, 1 hour TTL)
- **Mem0/Qdrant:** Long-term semantic memory (persistent)
- Enables follow-up questions and context retention
- Powers the "them/those/it" reference understanding

### 3. Multi-Step AI Pipeline
```
Question → Memory Retrieval → Schema RAG → SQL Generation →
Execution → Analysis → Insights → Memory Storage
```

### 4. Production Features
- Error handling and validation
- Query optimization suggestions
- Execution timing
- Session management
- User-provided API keys (secure testing)

---

## 📝 Complete Testing Checklist

### Functionality (40 points)

**SQL Generation (10 pts)**
- [ ] Generates valid SQLite syntax
- [ ] Handles SELECT queries correctly
- [ ] Handles JOIN queries correctly
- [ ] Handles aggregations (COUNT, SUM, AVG)
- [ ] Handles filtering (WHERE clauses)

**Query Execution (10 pts)**
- [ ] Returns actual data from database
- [ ] Formats results correctly (JSON)
- [ ] Handles empty results gracefully
- [ ] Shows execution time

**AI Explanations (10 pts)**
- [ ] Provides clear, beginner-friendly explanations
- [ ] Explains what the query does
- [ ] Relates explanation to the original question

**Conversation Memory (10 pts)**
- [ ] Remembers previous queries in same session
- [ ] Understands follow-up references ("them", "those", "it")
- [ ] Maintains context across multiple questions
- [ ] Different sessions are independent

### Technical Implementation (30 points)

**RAG Implementation (10 pts)**
- [ ] Retrieves relevant schema based on question
- [ ] Only includes necessary tables (not all)
- [ ] Semantic search works (understands intent)
- [ ] Reduces token usage efficiently

**Memory System (10 pts)**
- [ ] Redis short-term memory works
- [ ] Mem0 long-term memory works
- [ ] Combined context retrieval works
- [ ] Memory stats endpoint works

**Error Handling (10 pts)**
- [ ] Invalid SQL handled gracefully
- [ ] Missing API key shows clear error
- [ ] Database errors are caught
- [ ] Helpful error messages

### User Experience (20 points)

**API Design (10 pts)**
- [ ] Clear API documentation
- [ ] Easy to test via Swagger UI
- [ ] Sensible request/response format
- [ ] API key input is straightforward

**Output Quality (10 pts)**
- [ ] Insights are meaningful and relevant
- [ ] Optimizations are practical
- [ ] Response is well-structured
- [ ] All fields are populated

### Innovation (10 points)

**Advanced Features (5 pts)**
- [ ] Hybrid memory architecture (Redis + Mem0)
- [ ] RAG for schema retrieval
- [ ] Multi-step AI analysis
- [ ] Query optimization suggestions

**Overall Impression (5 pts)**
- [ ] Professional implementation
- [ ] Production-ready code quality
- [ ] Complete feature set
- [ ] Good documentation

**TOTAL: /100 points**

---

## 🧪 Sample Test Sequence

Copy and paste these one by one (remember to add your API key!):

### Test 1: Simple Query
```json
{
  "question": "Show me all customers",
  "session_id": "eval-1",
  "user_id": "teacher",
  "api_key": "YOUR_KEY_HERE"
}
```

### Test 2: Aggregation
```json
{
  "question": "How many orders do we have?",
  "session_id": "eval-2",
  "user_id": "teacher",
  "api_key": "YOUR_KEY_HERE"
}
```

### Test 3: Join Query
```json
{
  "question": "Show me customer names with their total purchase amounts",
  "session_id": "eval-3",
  "user_id": "teacher",
  "api_key": "YOUR_KEY_HERE"
}
```

### Test 4: Complex Analysis
```json
{
  "question": "What are the top 5 best-selling products by revenue?",
  "session_id": "eval-4",
  "user_id": "teacher",
  "api_key": "YOUR_KEY_HERE"
}
```

### Test 5a: Memory Test (First)
```json
{
  "question": "Show me products over $100",
  "session_id": "memory-eval",
  "user_id": "teacher",
  "api_key": "YOUR_KEY_HERE"
}
```

### Test 5b: Memory Test (Follow-up)
```json
{
  "question": "Now show only Electronics category",
  "session_id": "memory-eval",
  "user_id": "teacher",
  "api_key": "YOUR_KEY_HERE"
}
```
**This should filter the previous results to Electronics!**

### Test 5c: Memory Test (Another Follow-up)
```json
{
  "question": "Sort them by price descending",
  "session_id": "memory-eval",
  "user_id": "teacher",
  "api_key": "YOUR_KEY_HERE"
}
```
**Should remember BOTH previous filters and add sorting!**

---

## 🔐 Security & Privacy

**Your API Key is Safe:**
- ✅ Transmitted over HTTPS (encrypted)
- ✅ Used only for this specific request
- ✅ NOT stored in any database
- ✅ NOT logged anywhere
- ✅ Exists only in request memory

**Best Practices:**
- Use a test API key if you're concerned
- Monitor usage at: https://platform.openai.com/usage
- Full testing should cost less than $0.50

---

## 💰 Expected Costs (Your API Key)

**Per Query:**
- GPT-4 SQL generation: ~$0.01
- GPT-4 explanations: ~$0.01
- GPT-4 insights: ~$0.01
- Text embeddings: ~$0.001
- **Total per query: ~$0.03-0.05**

**Full Evaluation (20 queries):**
- Approximately: **$0.60 - $1.00**

**This is minimal cost for thorough testing!**

---

## 📊 Additional Endpoints to Test

### Memory Stats
**Endpoint:** `GET /rag/memory/stats`

**Parameters:**
- `session_id`: test-session
- `user_id`: teacher

**Shows:**
- Number of exchanges in Redis
- Number of memories in Mem0
- TTL information

### View All Memories
**Endpoint:** `GET /rag/memory/all/{user_id}`

**URL:** `https://nonconsuming-delly-dagny.ngrok-free.dev/rag/memory/all/teacher`

**Shows:**
- All long-term memories for the user
- Conversation patterns learned
- Preferences extracted

---

## 🛠️ Troubleshooting

### "Please enter your OpenAI API key first!"
- Make sure `api_key` field is included in your JSON
- Verify the key starts with `sk-`
- Check for copy-paste errors

### "Invalid API key" or 401 Error
- Double-check your OpenAI API key
- Make sure it's active (check OpenAI dashboard)
- Verify you have available credits

### "Failed to fetch" or Connection Error
- Check if the URL is still active
- Student's computer may be offline
- Student may have stopped the server

### Slow Response (>10 seconds)
- First query initializes everything (normal)
- Complex queries take longer (expected)
- GPT-4 API calls take 2-5 seconds each

### Empty Results
- Question may not match database schema
- Try simpler questions first
- Check the SQL query generated

---

## 📚 Database Schema Information

The app uses a sample **Retail Database** with:

**Tables:**
- `customers` (id, name, email, region)
- `products` (id, name, category, price, stock)
- `orders` (id, customer_id, order_date, total_amount)
- `order_items` (id, order_id, product_id, quantity, price)

**Sample Data:**
- 10+ customers across different regions
- 15+ products in various categories
- 20+ orders with line items

---

## ✅ Quick Evaluation Summary

**If all these work, the student deserves full marks:**

1. ✅ SQL queries are generated correctly
2. ✅ Results are returned from actual database
3. ✅ Explanations are clear and helpful
4. ✅ Conversation memory works (follow-ups work)
5. ✅ RAG retrieves relevant schemas only
6. ✅ AI insights are meaningful
7. ✅ Optimization suggestions make sense
8. ✅ Error handling is robust
9. ✅ API is well-documented
10. ✅ User can provide their own API key

---

## 🎯 Evaluation Rubric

**A+ (95-100):** All features work perfectly, excellent AI responses, robust memory
**A (90-94):** All core features work, good AI responses, memory mostly works
**B (80-89):** Most features work, decent AI responses, some memory issues
**C (70-79):** Basic features work, basic AI responses, memory limited
**Below C:** Significant features broken or missing

---

## 📞 Contact

**Project Repository:** https://github.com/SenayYakut/sql-query-buddy

**If Technical Issues:**
- Server not responding → Student's responsibility (computer offline)
- Invalid responses → May be temporary API issues
- Application errors → Student should fix

**For Clarifications:**
- Contact student: Senay Yakut
- Check repository README for architecture details

---

## 🎓 What This Project Demonstrates

**Technical Skills:**
- ✅ **AI/ML:** GPT-4 integration, prompt engineering
- ✅ **RAG:** Vector databases, semantic search
- ✅ **Backend:** FastAPI, Python, async programming
- ✅ **Databases:** SQLite, Redis, ChromaDB, Qdrant
- ✅ **Architecture:** Multi-tier memory system
- ✅ **API Design:** RESTful APIs, documentation
- ✅ **DevOps:** Deployment, environment configuration

**Advanced Concepts:**
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Hybrid memory architecture
- ✅ Vector embeddings and similarity search
- ✅ Context-aware AI systems
- ✅ Production-ready error handling

---

## 🚀 Start Testing Now!

**URL:** https://nonconsuming-delly-dagny.ngrok-free.dev/docs

1. Click the URL
2. Find "POST /rag/query"
3. Click "Try it out"
4. Paste your API key
5. Ask a question
6. See the magic! ✨

---

**Expected Testing Time:** 15-20 minutes for thorough evaluation

**Have fun exploring the AI-powered SQL assistant!** 🤖

---

*Note: This is a live deployment. The URL will remain active as long as the student's application is running.*
