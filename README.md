# 🤖 Telegram Search Bot

A comprehensive Python-based Telegram bot that provides powerful search capabilities across multiple sources including web search, Wikipedia, news, and images.

## ✨ Features

- 🔍 **Web Search** - Search the internet using DuckDuckGo
- 📚 **Wikipedia Search** - Access Wikipedia articles with summaries
- 📰 **News Search** - Find latest news articles
- 🖼️ **Image Search** - Search for images with preview links
- 🤖 **Interactive Interface** - Inline keyboards for easy navigation
- 🔄 **Real-time Results** - Fast, asynchronous search processing

## 🚀 Quick Start

### 1. Create a Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Save your **Bot Token**

### 2. Set Up the Bot
```bash
# Clone or download the files
cd telegram-search-bot

# Run the setup script (recommended)
./start_bot.sh
```

### 3. Configure
```bash
# Copy environment template
cp .env.example .env

# Edit with your bot token
nano .env
# Add: TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 4. Run
```bash
# Start the bot
./start_bot.sh

# Or run directly
python telegram_search_bot.py
```

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message and features overview | `/start` |
| `/help` | Show all available commands | `/help` |
| `/search` | Search the web | `/search python programming` |
| `/wiki` | Search Wikipedia | `/wiki artificial intelligence` |
| `/news` | Search for news | `/news latest technology` |
| `/image` | Search for images | `/image sunset mountains` |

## 📁 Project Structure

```
telegram-search-bot/
├── telegram_search_bot.py    # Main bot application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── start_bot.sh            # Setup and startup script
├── test_bot.py             # Test script to verify setup
├── SETUP_GUIDE.md          # Detailed setup instructions
└── README.md               # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+ 
- pip (Python package manager)
- A Telegram account

### Dependencies
The bot uses these Python packages:
- `python-telegram-bot` - Telegram Bot API wrapper
- `aiohttp` - Async HTTP client for web requests
- `beautifulsoup4` - HTML parsing for search results
- `wikipedia` - Wikipedia API access
- `requests` - HTTP library for API calls

### Setup Options

#### Option 1: Automated Setup (Recommended)
```bash
./start_bot.sh
```

#### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export TELEGRAM_BOT_TOKEN="your_bot_token"

# Run bot
python telegram_search_bot.py
```

## 🧪 Testing

Test your setup before running:
```bash
./test_bot.py
```

This will verify:
- Python version compatibility
- All dependencies are installed
- Bot module can be imported
- Environment variables are set

## 💡 Usage Examples

### Basic Search
Send any message to get search options:
```
User: "machine learning"
Bot: [Shows buttons for Web, Wikipedia, News, Image search]
```

### Direct Commands
```bash
/search how to learn python
/wiki quantum computing  
/news artificial intelligence 2024
/image beautiful landscape
```

### Interactive Features
- Inline keyboard buttons for easy searching
- "Search Again" functionality
- Error handling with helpful messages
- Formatted results with clickable links

## 🔧 Advanced Configuration

### Environment Variables
```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token

# Optional (for enhanced features)
NEWS_API_KEY=your_news_api_key
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

### Running as a Service
See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:
- Systemd service configuration
- Docker deployment
- Production deployment tips

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
- Check if bot token is correct
- Verify bot is running: `ps aux | grep telegram_search_bot`
- Check logs: `tail -f bot.log`

**Import errors:**
```bash
pip install -r requirements.txt
```

**Permission denied:**
```bash
chmod +x start_bot.sh
chmod +x test_bot.py
```

## 📊 Features Overview

### Search Capabilities
- **Web Search**: Uses DuckDuckGo for privacy-focused web search
- **Wikipedia**: Full Wikipedia integration with disambiguation handling
- **News Search**: Latest news articles from multiple sources
- **Image Search**: Image results with preview capabilities

### User Experience
- **Intuitive Interface**: Easy-to-use commands and buttons
- **Fast Results**: Asynchronous processing for quick responses
- **Error Handling**: Graceful error handling with user feedback
- **Responsive Design**: Works well on mobile and desktop Telegram

### Technical Features
- **Async/Await**: Modern Python async programming
- **Error Recovery**: Robust error handling and logging
- **Extensible**: Easy to add new search sources
- **Secure**: Environment-based configuration

## 🔒 Security & Privacy

- Bot tokens stored in environment variables
- No user data collection or storage
- Uses privacy-focused search engines
- Secure HTTP requests with proper headers

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup instructions
- [requirements.txt](requirements.txt) - Python dependencies
- [.env.example](.env.example) - Environment configuration template

## 🎯 Next Steps

1. **Customize** the bot responses and add more features
2. **Deploy** to a server for 24/7 availability  
3. **Monitor** usage and performance
4. **Extend** with additional search sources or commands

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and enhancement requests.

---

**Ready to search? Start your bot and enjoy! 🚀**
