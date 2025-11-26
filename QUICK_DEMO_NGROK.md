# Quick Demo Setup with ngrok

Share your local app with others in 5 minutes using ngrok.

---

## What You'll Get:

✅ Your app running locally
✅ Public HTTPS URL anyone can access
✅ Perfect for quick demos/testing
✅ Free (with limits)

---

## Step 1: Install ngrok

### Mac:
```bash
brew install ngrok
```

### Windows/Linux:
1. Go to: https://ngrok.com/download
2. Download and extract
3. Add to PATH

### Create ngrok Account (Free):
1. Go to: https://dashboard.ngrok.com/signup
2. Sign up (free)
3. Copy your authtoken
4. Run: `ngrok config add-authtoken YOUR_TOKEN`

---

## Step 2: Start Your App with Docker

```bash
cd /Users/senayyakut/Desktop/sql-query-buddy

# Make sure .env file exists with your OpenAI key
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY

# Start with Docker
docker-compose up
```

**Wait until you see:**
```
frontend_1  | Compiled successfully!
backend_1   | Uvicorn running on http://0.0.0.0:8000
```

---

## Step 3: Expose to Internet with ngrok

**Open a NEW terminal window:**

```bash
# Expose port 3000 (frontend)
ngrok http 3000
```

**You'll see:**
```
Session Status    online
Account           Your Name (Plan: Free)
Forwarding        https://a1b2c3d4.ngrok.io -> http://localhost:3000
```

---

## Step 4: Share Your App!

**Copy the HTTPS URL** (looks like: `https://a1b2c3d4.ngrok.io`)

**Share it with:**
- Contest judges
- Teammates
- Anyone who needs to test
- Put it in your presentation

**They can access:**
- Frontend: `https://a1b2c3d4.ngrok.io`
- Try queries, see results
- No installation needed!

---

## Important Notes:

### Free Tier Limits:
- ⏰ **2 hour session limit** (restart ngrok to continue)
- 🔗 **URL changes** each time you restart
- 👥 **40 connections/min** limit
- 📊 Limited data transfer

### Keep Running:
- ✅ Keep Docker running
- ✅ Keep ngrok running
- ✅ Keep your computer on
- ✅ Keep internet connected

---

## Alternative: Expose Backend Too

If you want to expose the backend API docs:

**Terminal 1:**
```bash
# Frontend
ngrok http 3000
```

**Terminal 2:**
```bash
# Backend API
ngrok http 8000
```

Now you have two URLs:
- Frontend: `https://abc123.ngrok.io`
- Backend API: `https://xyz789.ngrok.io/docs`

---

## Troubleshooting:

### URL not working?
- Make sure Docker is running: `docker-compose ps`
- Make sure ngrok is running
- Check ngrok dashboard: https://dashboard.ngrok.com/

### Session expired?
```bash
# Stop ngrok (Ctrl+C)
# Restart it
ngrok http 3000
# You'll get a NEW URL - share the new one
```

### Too slow?
- Free tier has bandwidth limits
- Consider deploying to Oracle Cloud for better performance

---

## When to Use ngrok:

✅ **Good for:**
- Quick demos (1-2 hours)
- Testing with teammates
- Showing to 1-2 people
- Development sharing

❌ **Not good for:**
- Multi-day contests
- Many concurrent users
- Production use
- Permanent URLs

**For longer contests → Use Oracle Cloud instead!**

---

## Upgrade Options:

### ngrok Free:
- 1 online process
- 40 connections/min
- Random URLs
- 2 hour sessions

### ngrok Pro ($10/month):
- Custom subdomains
- No time limits
- Reserved domains
- More connections

**Still cheaper than cloud hosting for short-term use!**

---

## Summary:

```bash
# 1. Start your app
docker-compose up

# 2. In new terminal, expose it
ngrok http 3000

# 3. Share the URL
https://random123.ngrok.io

# 4. Demo your app!
```

**Time to setup:** 5 minutes
**Cost:** Free
**Works for:** Quick demos and testing

---

**For permanent deployment, see: ORACLE_CLOUD_SETUP.md**
