#!/bin/bash

# Quick Start Script for Telegram Search Bot
# This script automates the entire setup process

clear
echo "🚀 Telegram Search Bot - Quick Start"
echo "====================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "🐍 Python version: $PYTHON_VERSION"

# Step 1: Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "📋 Step 1: Setting up environment configuration"
    echo "=============================================="
    
    if [ ! -f ".env.example" ]; then
        echo "❌ .env.example not found!"
        exit 1
    fi
    
    cp .env.example .env
    echo "✅ Created .env file from template"
    
    echo ""
    echo "⚠️  IMPORTANT: You need to add your Telegram Bot Token!"
    echo ""
    echo "🔑 How to get a bot token:"
    echo "1. Open Telegram and search for @BotFather"
    echo "2. Send /newbot command"
    echo "3. Follow the instructions to create your bot"
    echo "4. Copy the bot token BotFather gives you"
    echo ""
    echo "📝 Now edit the .env file and add your token:"
    echo "nano .env"
    echo ""
    read -p "Press Enter after you've added your bot token to .env file..."
fi

# Step 2: Set up virtual environment
echo ""
echo "📦 Step 2: Setting up Python environment"
echo "========================================"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Step 3: Install dependencies
echo ""
echo "📥 Step 3: Installing dependencies"
echo "================================="

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo "Installing Python packages..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed successfully"

# Step 4: Test setup
echo ""
echo "🧪 Step 4: Testing setup"
echo "======================="

if [ -f "test_bot.py" ]; then
    echo "Running tests..."
    python test_bot.py
    TEST_RESULT=$?
    
    if [ $TEST_RESULT -eq 0 ]; then
        echo "✅ All tests passed!"
    else
        echo "❌ Some tests failed. Please check the output above."
        echo "Common issues:"
        echo "- Bot token not set in .env file"
        echo "- Missing dependencies"
        echo "- Python version too old"
        exit 1
    fi
else
    echo "⚠️  Test script not found, skipping tests"
fi

# Step 5: Check bot token
echo ""
echo "🔧 Step 5: Verifying configuration"
echo "================================="

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN is not set!"
    echo ""
    echo "Please edit your .env file and add your bot token:"
    echo "nano .env"
    echo ""
    echo "Add this line:"
    echo "TELEGRAM_BOT_TOKEN=your_bot_token_here"
    exit 1
else
    echo "✅ Bot token is configured"
fi

# Step 6: Ready to run
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Your Telegram Search Bot is ready to run!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure you have your bot token in .env file"
echo "2. Run the bot: ./start_bot.sh"
echo "3. Go to Telegram and start chatting with your bot"
echo ""
echo "💡 Commands your bot supports:"
echo "• /start - Welcome message"
echo "• /help - Show help"
echo "• /search <query> - Web search"
echo "• /wiki <query> - Wikipedia search"
echo "• /news <query> - News search"
echo "• /image <query> - Image search"
echo ""
echo "🚀 To start your bot now, run:"
echo "./start_bot.sh"
echo ""

# Ask if user wants to start the bot immediately
read -p "Would you like to start the bot now? (y/N): " START_NOW

if [[ $START_NOW =~ ^[Yy]$ ]]; then
    echo ""
    echo "🤖 Starting your Telegram Search Bot..."
    echo "Press Ctrl+C to stop the bot when you're done testing"
    echo ""
    sleep 2
    
    # Start the bot
    python telegram_search_bot.py
else
    echo ""
    echo "👋 Setup complete! Run './start_bot.sh' when you're ready to start your bot."
fi