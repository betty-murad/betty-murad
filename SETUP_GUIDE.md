# 🤖 Telegram Search Bot - Complete Setup Guide

This guide will walk you through setting up a fully functional Telegram search bot with Python.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Creating a Telegram Bot](#creating-a-telegram-bot)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Bot](#running-the-bot)
6. [Features](#features)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

## 🛠️ Prerequisites

Before starting, make sure you have:
- Python 3.8 or higher installed
- A Telegram account
- Basic command line knowledge
- Internet connection

### Check Python Version
```bash
python3 --version
```

If Python is not installed, visit [python.org](https://python.org) to download it.

## 🔑 Creating a Telegram Bot

### Step 1: Contact BotFather
1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather
3. Send `/newbot` command

### Step 2: Create Your Bot
1. Choose a name for your bot (e.g., "My Search Bot")
2. Choose a username ending in "bot" (e.g., "my_search_bot")
3. BotFather will provide you with a **Bot Token** - SAVE THIS!

**Example Bot Token:** `1234567890:ABCDEFGHijklmnopqrstuvwxyz123456789`

### Step 3: Configure Bot Settings (Optional)
```
/setdescription - Set bot description
/setabouttext - Set about text
/setuserpic - Set bot profile picture
/setcommands - Set command list
```

**Recommended Commands to Set:**
```
start - Start the bot and see welcome message
help - Show help and available commands
search - Search the web for any topic
wiki - Search Wikipedia articles
news - Search for latest news
image - Search for images
```

## 📦 Installation

### Step 1: Clone/Download the Bot Files
If you have the files, navigate to the bot directory:
```bash
cd /path/to/telegram-search-bot
```

### Step 2: Install Dependencies
You have two options:

#### Option A: Using the Startup Script (Recommended)
```bash
./start_bot.sh
```
This script will automatically:
- Create a virtual environment
- Install all dependencies
- Guide you through configuration

#### Option B: Manual Installation
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Create Environment File
```bash
cp .env.example .env
```

### Step 2: Add Your Bot Token
Edit the `.env` file:
```bash
nano .env
```

Add your bot token:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHijklmnopqrstuvwxyz123456789
```

**Security Note:** Never share your bot token or commit it to version control!

### Step 3: Set Environment Variable (Alternative)
Instead of using `.env` file, you can set the environment variable directly:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

## 🚀 Running the Bot

### Option 1: Using Startup Script
```bash
./start_bot.sh
```

### Option 2: Direct Python Execution
```bash
# Activate virtual environment first
source venv/bin/activate

# Run the bot
python telegram_search_bot.py
```

### Option 3: Background Execution
To run the bot in the background:
```bash
nohup python telegram_search_bot.py > bot.log 2>&1 &
```

## ✨ Features

Your bot supports these commands:

### 🔍 Web Search
- `/search python programming` - Search the web
- Just send any text message for quick search options

### 📚 Wikipedia Search
- `/wiki artificial intelligence` - Search Wikipedia
- Handles disambiguation automatically
- Shows related articles

### 📰 News Search
- `/news latest technology` - Search for news
- Returns recent articles with dates

### 🖼️ Image Search
- `/image beautiful sunset` - Search for images
- Returns image links and dimensions

### 🤖 Interactive Features
- Inline keyboard buttons for easy searching
- Search suggestions and demos
- Error handling and user feedback

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Bot Token Error
```
❌ Error: TELEGRAM_BOT_TOKEN environment variable not set!
```
**Solution:** Make sure your `.env` file exists and contains the correct token.

#### Import Errors
```
ModuleNotFoundError: No module named 'telegram'
```
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

#### Permission Denied
```
bash: ./start_bot.sh: Permission denied
```
**Solution:** Make the script executable:
```bash
chmod +x start_bot.sh
```

#### Bot Not Responding
1. Check if the bot is running: `ps aux | grep telegram_search_bot`
2. Check logs for errors: `tail -f bot.log`
3. Verify bot token is correct
4. Ensure bot is not blocked in Telegram

#### Network Issues
```
aiohttp.client_exceptions.ClientError
```
**Solution:** Check internet connection and firewall settings.

### Debugging Tips

#### Enable Debug Logging
Edit `telegram_search_bot.py` and change:
```python
level=logging.INFO
```
to:
```python
level=logging.DEBUG
```

#### Test Bot Token
```bash
curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"
```

## 🔧 Advanced Configuration

### Adding More Search Engines

You can extend the bot with additional search engines:

#### Google Search API
1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Create Custom Search Engine
3. Add to `.env`:
```
GOOGLE_SEARCH_API_KEY=your_api_key
GOOGLE_SEARCH_ENGINE_ID=your_engine_id
```

#### News API
1. Get API key from [NewsAPI](https://newsapi.org/)
2. Add to `.env`:
```
NEWS_API_KEY=your_news_api_key
```

### Running as a Service (Linux)

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/telegram-search-bot.service
```

```ini
[Unit]
Description=Telegram Search Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram-search-bot
Environment=TELEGRAM_BOT_TOKEN=your_bot_token
ExecStart=/path/to/telegram-search-bot/venv/bin/python telegram_search_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable telegram-search-bot
sudo systemctl start telegram-search-bot
sudo systemctl status telegram-search-bot
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY telegram_search_bot.py .
CMD ["python", "telegram_search_bot.py"]
```

Build and run:
```bash
docker build -t telegram-search-bot .
docker run -e TELEGRAM_BOT_TOKEN=your_token telegram-search-bot
```

## 📝 Usage Examples

### Basic Commands
```
/start                          # Welcome message
/help                           # Show help
/search machine learning        # Web search
/wiki quantum computing         # Wikipedia search
/news artificial intelligence   # News search
/image mountain landscape       # Image search
```

### Interactive Usage
1. Send any text message to the bot
2. Choose search type from inline buttons
3. Get formatted results with links
4. Use "Search Again" buttons for new queries

## 🔒 Security Best Practices

1. **Never share your bot token**
2. **Use environment variables for secrets**
3. **Don't commit `.env` files to git**
4. **Regularly rotate your bot token**
5. **Monitor bot usage logs**
6. **Use HTTPS for webhooks (production)**

## 📊 Monitoring and Logs

### View Logs
```bash
tail -f bot.log
```

### Monitor Performance
```bash
# Check memory usage
ps aux | grep telegram_search_bot

# Check network connections
netstat -an | grep python
```

## 🎯 Next Steps

1. **Test your bot** with various search queries
2. **Customize responses** by editing the bot code
3. **Add more features** like weather, currency conversion
4. **Deploy to a server** for 24/7 availability
5. **Monitor usage** and optimize performance

## 📞 Support

If you encounter issues:
1. Check this guide first
2. Review the error logs
3. Test with simple queries
4. Verify your bot token
5. Check your internet connection

## 🎉 Congratulations!

Your Telegram Search Bot is now ready to use! Start chatting with your bot and enjoy searching across multiple sources directly from Telegram.

---

**Happy Searching! 🚀**