#!/usr/bin/env python3
"""
Telegram Search Bot
A comprehensive search bot that can perform web searches, Wikipedia searches, and news searches.
"""

import os
import logging
import asyncio
import aiohttp
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import wikipedia
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramSearchBot:
    def __init__(self, token: str):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up command and message handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("search", self.web_search))
        self.app.add_handler(CommandHandler("wiki", self.wikipedia_search))
        self.app.add_handler(CommandHandler("news", self.news_search))
        self.app.add_handler(CommandHandler("image", self.image_search))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 **Welcome to Search Bot!**

I can help you search for information across multiple sources:

**Available Commands:**
🔍 `/search <query>` - Web search
📚 `/wiki <query>` - Wikipedia search  
📰 `/news <query>` - News search
🖼️ `/image <query>` - Image search
❓ `/help` - Show this help message

**Quick Search:**
Just send me any message and I'll search for it!

**Examples:**
• `/search python programming`
• `/wiki artificial intelligence`
• `/news latest technology`
• `bitcoin price` (direct message)
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔍 Web Search", callback_data="search_demo"),
                InlineKeyboardButton("📚 Wikipedia", callback_data="wiki_demo")
            ],
            [
                InlineKeyboardButton("📰 News", callback_data="news_demo"),
                InlineKeyboardButton("🖼️ Images", callback_data="image_demo")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
📋 **Search Bot Help**

**Commands:**
• `/start` - Welcome message
• `/search <query>` - Search the web
• `/wiki <query>` - Search Wikipedia
• `/news <query>` - Search for news
• `/image <query>` - Search for images
• `/help` - Show this help

**Usage Examples:**
```
/search how to learn python
/wiki quantum computing
/news climate change 2024
/image sunset mountains
```

**Direct Search:**
Send any text message without a command and I'll perform a web search!

**Tips:**
• Be specific with your queries for better results
• Use quotes for exact phrases: "machine learning"
• Add location for local searches: pizza near me
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def web_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Perform web search using DuckDuckGo"""
        if not context.args:
            await update.message.reply_text("Please provide a search query!\nExample: `/search python programming`")
            return
        
        query = ' '.join(context.args)
        await update.message.reply_text(f"🔍 Searching for: *{query}*...", parse_mode='Markdown')
        
        try:
            results = await self._duckduckgo_search(query)
            if results:
                response = f"🔍 **Search Results for:** {query}\n\n"
                for i, result in enumerate(results[:5], 1):
                    response += f"**{i}. {result['title']}**\n"
                    response += f"{result['snippet']}\n"
                    response += f"🔗 {result['url']}\n\n"
                
                keyboard = [[InlineKeyboardButton("🔍 Search Again", callback_data=f"search_{query}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    response,
                    parse_mode='Markdown',
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
            else:
                await update.message.reply_text("❌ No results found. Try a different search query.")
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            await update.message.reply_text("❌ Search failed. Please try again later.")
    
    async def wikipedia_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search Wikipedia"""
        if not context.args:
            await update.message.reply_text("Please provide a search query!\nExample: `/wiki artificial intelligence`")
            return
        
        query = ' '.join(context.args)
        await update.message.reply_text(f"📚 Searching Wikipedia for: *{query}*...", parse_mode='Markdown')
        
        try:
            # Set language to English
            wikipedia.set_lang("en")
            
            # Search for articles
            search_results = wikipedia.search(query, results=3)
            
            if not search_results:
                await update.message.reply_text("❌ No Wikipedia articles found.")
                return
            
            # Get the first result
            page = wikipedia.page(search_results[0])
            
            # Prepare response
            summary = wikipedia.summary(search_results[0], sentences=3)
            response = f"📚 **Wikipedia: {page.title}**\n\n"
            response += f"{summary}\n\n"
            response += f"🔗 [Read full article]({page.url})"
            
            # Add related articles if available
            if len(search_results) > 1:
                response += f"\n\n**Related articles:**\n"
                for article in search_results[1:]:
                    response += f"• {article}\n"
            
            keyboard = [[InlineKeyboardButton("📚 Search Wikipedia Again", callback_data=f"wiki_{query}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                response,
                parse_mode='Markdown',
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation
            options = e.options[:5]  # Show first 5 options
            response = f"📚 **Multiple articles found for:** {query}\n\n"
            response += "**Did you mean:**\n"
            for option in options:
                response += f"• {option}\n"
            
            await update.message.reply_text(response, parse_mode='Markdown')
        
        except wikipedia.exceptions.PageError:
            await update.message.reply_text("❌ Wikipedia page not found. Try a different search term.")
        
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            await update.message.reply_text("❌ Wikipedia search failed. Please try again.")
    
    async def news_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search for news articles"""
        if not context.args:
            await update.message.reply_text("Please provide a search query!\nExample: `/news technology trends`")
            return
        
        query = ' '.join(context.args)
        await update.message.reply_text(f"📰 Searching news for: *{query}*...", parse_mode='Markdown')
        
        try:
            results = await self._news_search(query)
            if results:
                response = f"📰 **Latest News for:** {query}\n\n"
                for i, article in enumerate(results[:5], 1):
                    response += f"**{i}. {article['title']}**\n"
                    response += f"📅 {article['date']}\n"
                    response += f"{article['snippet']}\n"
                    response += f"🔗 {article['url']}\n\n"
                
                keyboard = [[InlineKeyboardButton("📰 Search News Again", callback_data=f"news_{query}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    response,
                    parse_mode='Markdown',
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
            else:
                await update.message.reply_text("❌ No news articles found. Try a different search query.")
        
        except Exception as e:
            logger.error(f"News search error: {e}")
            await update.message.reply_text("❌ News search failed. Please try again later.")
    
    async def image_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search for images"""
        if not context.args:
            await update.message.reply_text("Please provide a search query!\nExample: `/image sunset landscape`")
            return
        
        query = ' '.join(context.args)
        await update.message.reply_text(f"🖼️ Searching images for: *{query}*...", parse_mode='Markdown')
        
        try:
            results = await self._image_search(query)
            if results:
                response = f"🖼️ **Image Results for:** {query}\n\n"
                for i, image in enumerate(results[:3], 1):
                    response += f"**{i}. {image['title']}**\n"
                    response += f"🔗 [View Image]({image['url']})\n"
                    response += f"📐 {image['dimensions']}\n\n"
                
                keyboard = [[InlineKeyboardButton("🖼️ Search Images Again", callback_data=f"image_{query}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    response,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text("❌ No images found. Try a different search query.")
        
        except Exception as e:
            logger.error(f"Image search error: {e}")
            await update.message.reply_text("❌ Image search failed. Please try again later.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages as search queries"""
        query = update.message.text
        
        # Show search options
        keyboard = [
            [
                InlineKeyboardButton("🔍 Web Search", callback_data=f"search_{query}"),
                InlineKeyboardButton("📚 Wikipedia", callback_data=f"wiki_{query}")
            ],
            [
                InlineKeyboardButton("📰 News", callback_data=f"news_{query}"),
                InlineKeyboardButton("🖼️ Images", callback_data=f"image_{query}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🔍 What would you like to search for: *{query}*?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button presses"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("search_"):
            search_query = data[7:]  # Remove "search_" prefix
            context.args = search_query.split()
            await self.web_search(update, context)
        
        elif data.startswith("wiki_"):
            search_query = data[5:]  # Remove "wiki_" prefix
            context.args = search_query.split()
            await self.wikipedia_search(update, context)
        
        elif data.startswith("news_"):
            search_query = data[5:]  # Remove "news_" prefix
            context.args = search_query.split()
            await self.news_search(update, context)
        
        elif data.startswith("image_"):
            search_query = data[6:]  # Remove "image_" prefix
            context.args = search_query.split()
            await self.image_search(update, context)
        
        elif data.endswith("_demo"):
            demo_type = data.replace("_demo", "")
            demo_queries = {
                "search": "python programming",
                "wiki": "artificial intelligence",
                "news": "latest technology",
                "image": "beautiful landscape"
            }
            await query.edit_message_text(
                f"Try: `/{demo_type} {demo_queries[demo_type]}`",
                parse_mode='Markdown'
            )
    
    async def _duckduckgo_search(self, query: str, max_results: int = 5):
        """Perform web search using DuckDuckGo"""
        try:
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }) as response:
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result')[:max_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('div', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text().strip()
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text().strip()
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
            
            return results
        
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return []
    
    async def _news_search(self, query: str, max_results: int = 5):
        """Search for news articles"""
        try:
            # Using DuckDuckGo news search
            url = "https://html.duckduckgo.com/html/"
            params = {"q": f"{query} site:news", "iar": "news"}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }) as response:
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result')[:max_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('div', class_='result__snippet')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text().strip()
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text().strip()
                    date = "Recent"  # Could be enhanced to extract actual dates
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet,
                        'date': date
                    })
            
            return results
        
        except Exception as e:
            logger.error(f"News search error: {e}")
            return []
    
    async def _image_search(self, query: str, max_results: int = 3):
        """Search for images"""
        try:
            # Simple implementation - returns placeholder results
            # In production, you'd use a proper image search API
            results = []
            for i in range(max_results):
                results.append({
                    'title': f'Image result {i+1} for {query}',
                    'url': f'https://picsum.photos/800/600?random={hash(query + str(i)) % 1000}',
                    'dimensions': '800x600'
                })
            return results
        
        except Exception as e:
            logger.error(f"Image search error: {e}")
            return []
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram Search Bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    # Get bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set your bot token: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        return
    
    # Create and run bot
    bot = TelegramSearchBot(token)
    bot.run()

if __name__ == '__main__':
    main()