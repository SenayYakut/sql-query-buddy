# Teacher Testing Guide 🎓

Quick guide for teachers to test SQL Query Buddy using their own OpenAI API key.

---

## What You'll Need

1. **OpenAI API Key** - Get it at: https://platform.openai.com/api-keys
2. **The App URL** - Student will provide (something like `https://abc123.ngrok.io`)

---

## Step-by-Step Testing Instructions

### Step 1: Open the App

Click the URL provided by the student (e.g., `https://abc123.ngrok.io`)

You'll see the SQL Query Buddy interface with a purple gradient header.

### Step 2: Enter Your OpenAI API Key

**At the top of the page, you'll see a yellow box:**

```
🔑 OpenAI API Key: [Show/Hide Button]
[Enter your OpenAI API key (sk-...)]
💡 Your API key is only used for this session and never stored
```

**Actions:**
1. Click in the text field
2. Paste your OpenAI API key (starts with `sk-proj-...` or `sk-...`)
3. The key is hidden by default (shows as `••••••`)
4. Click "Show" button if you want to verify it

**Important:**
- ✅ Your key is only used for THIS testing session
- ✅ It's NOT saved anywhere
- ✅ It's sent securely over HTTPS
- ✅ Only YOU will be charged for API usage, not the student

### Step 3: Ask a Question

**Type a question in the main input field:**

Try one of the example questions:
- "Show me the top 5 customers by total purchase amount"
- "List products with prices above $100"
- "Which customer has the highest total purchase?"

**Or ask your own question!**

### Step 4: Review the Results

After clicking "Ask", you'll see:

1. **Generated SQL Query** (in green/black code block)
2. **Query Explanation** (simple English explanation)
3. **Results Table** (actual data from the database)
4. **AI Insights** (analysis of the data)
5. **Optimization Suggestions** (performance tips)

### Step 5: Test Conversation Memory (Optional)

The app remembers your conversation! Try this:

**First question:**
```
"Show me the top 5 customers"
```

**Second question (follow-up):**
```
"Now filter them to California only"
```

The app understands "them" refers to the previous top 5 customers!

---

## What to Evaluate

### ✅ Technical Features:
- [ ] SQL query generation works correctly
- [ ] Results are accurate and properly formatted
- [ ] AI explanations are clear and helpful
- [ ] Conversation memory works (follow-up questions)
- [ ] Query optimization suggestions are relevant
- [ ] Response time is reasonable (a few seconds)

### ✅ User Experience:
- [ ] Interface is clean and intuitive
- [ ] API key input is clear and secure
- [ ] Error messages are helpful
- [ ] Example questions help users get started

### ✅ AI/RAG Capabilities:
- [ ] Understands natural language questions
- [ ] Generates correct SQL syntax
- [ ] Retrieves relevant database schema
- [ ] Provides meaningful insights from data
- [ ] Remembers conversation context

---

## Example Test Scenarios

### Scenario 1: Basic Query
**Question:** "Show me all customers"
**Expected:** Simple SELECT query with customer data

### Scenario 2: Aggregation
**Question:** "What's the average product price?"
**Expected:** Uses AVG() function correctly

### Scenario 3: Joins
**Question:** "Show me orders with customer names"
**Expected:** Properly joins orders and customers tables

### Scenario 4: Conversation Memory
**Question 1:** "Show top 5 products"
**Question 2:** "Filter them by category Electronics"
**Expected:** Remembers previous query context

---

## Troubleshooting

### "Please enter your OpenAI API key first!"
- Make sure you've pasted your key in the yellow box at the top
- Verify the key starts with `sk-`

### "Failed to fetch results"
- Check if the backend is running (student's responsibility)
- Verify your internet connection
- Make sure your API key is valid

### "Invalid API key" or Authentication Error
- Double-check your OpenAI API key
- Make sure it's active and has available credits
- Verify you copied the entire key

### Slow Response
- First query may take 5-10 seconds (initializing)
- Complex queries with joins may take longer
- This is normal for AI-powered SQL generation

---

## Security Notes for Teachers

**Your API Key is Safe:**
- ✅ Transmitted over HTTPS (encrypted)
- ✅ NOT stored in any database
- ✅ NOT logged or saved
- ✅ Only exists in browser memory during session
- ✅ Disappears when you close the browser tab

**Best Practice:**
- Use a test API key with usage limits if concerned
- Monitor your OpenAI usage at: https://platform.openai.com/usage
- Testing this app should cost less than $0.10

---

## Cost Information

**Typical testing costs (with your API key):**
- 5 queries: ~$0.02 - $0.05
- 20 queries: ~$0.10 - $0.20
- Full evaluation: ~$0.20 - $0.50

**Uses:**
- GPT-4 for SQL generation
- GPT-4 for explanations and insights
- Text embeddings for schema retrieval

---

## Sample Questions to Try

### Easy:
- "Show me all products"
- "How many customers do we have?"
- "List all orders"

### Medium:
- "What's the total revenue?"
- "Show me the top 5 best-selling products"
- "Which customers spent the most money?"

### Advanced:
- "Show me monthly revenue trends"
- "Find customers who haven't ordered in the last 30 days"
- "What's the average order value by customer region?"

### Testing Memory:
1. "Show me products over $100"
2. "Now show only Electronics category" ← Tests context memory
3. "Sort them by price descending" ← Tests continued context

---

## Evaluation Checklist

### Functionality (40 points)
- [ ] Correctly generates SQL queries (10 pts)
- [ ] Executes queries and shows results (10 pts)
- [ ] Provides helpful explanations (10 pts)
- [ ] Conversation memory works (10 pts)

### Technical Implementation (30 points)
- [ ] RAG (schema retrieval) works (10 pts)
- [ ] AI insights are meaningful (10 pts)
- [ ] Error handling is robust (10 pts)

### User Experience (20 points)
- [ ] Interface is intuitive (10 pts)
- [ ] API key input is clear and secure (10 pts)

### Innovation (10 points)
- [ ] Creative use of AI/RAG (5 pts)
- [ ] Advanced features (memory, optimization) (5 pts)

**Total: /100 points**

---

## Contact Student

If you encounter any technical issues:
- The backend may not be running
- Network/connection issues
- Configuration problems

These are the student's responsibility to fix!

---

## Quick Reference

**Get OpenAI API Key:** https://platform.openai.com/api-keys
**Check Usage:** https://platform.openai.com/usage
**OpenAI Pricing:** https://openai.com/api/pricing/

**Expected Behavior:**
1. Enter API key ✅
2. Ask question ✅
3. Get SQL + Results + Insights ✅
4. Follow-up questions remember context ✅

---

**Happy Testing! 🚀**

If everything works as described above, the student has built a functional RAG-powered SQL assistant with conversation memory!
