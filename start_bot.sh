#!/bin/bash

# Telegram Search Bot Startup Script

echo "🤖 Starting Telegram Search Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📋 Please create a .env file based on .env.example"
    echo "💡 You can copy .env.example to .env and add your bot token"
    echo ""
    echo "To create your .env file:"
    echo "cp .env.example .env"
    echo "nano .env"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to stop and configure .env first..."
fi

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "🔧 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if bot token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN not set!"
    echo "Please set your bot token:"
    echo "export TELEGRAM_BOT_TOKEN='your_bot_token_here'"
    echo ""
    echo "Or add it to your .env file"
    exit 1
fi

# Start the bot
echo "🚀 Starting bot..."
python telegram_search_bot.py