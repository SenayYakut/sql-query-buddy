#!/bin/bash

echo "=================================="
echo "🚀 Starting SQL Query Buddy"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Creating .env file..."
    cp .env.example .env
    echo ""
    echo "❗ IMPORTANT: Edit .env file and add your OpenAI API key!"
    echo "   Run: nano .env"
    echo "   Then run this script again."
    exit 1
fi

# Check if OpenAI key is set
if grep -q "your_openai_api_key_here" .env; then
    echo "❗ IMPORTANT: Your .env file needs your OpenAI API key!"
    echo "   Run: nano .env"
    echo "   Replace 'your_openai_api_key_here' with your actual key"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Start Docker Compose
echo "📦 Starting Docker containers..."
echo ""
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "=================================="
echo "✅ SQL Query Buddy is running!"
echo "=================================="
echo ""
echo "📍 Local access:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "=================================="
echo "🌐 To share with your teacher:"
echo "=================================="
echo ""
echo "In a NEW terminal window, run:"
echo ""
echo "   ngrok http 3000"
echo ""
echo "Then share the HTTPS URL with your teacher!"
echo ""
echo "=================================="
echo ""
echo "📋 Useful commands:"
echo "   View logs:  docker-compose logs -f"
echo "   Stop:       docker-compose down"
echo ""
