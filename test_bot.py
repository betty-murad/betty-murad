#!/usr/bin/env python3
"""
Test script for Telegram Search Bot
This script tests if all dependencies are installed correctly.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import telegram: {e}")
        return False
    
    try:
        import aiohttp
        print("✅ aiohttp imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import aiohttp: {e}")
        return False
    
    try:
        import wikipedia
        print("✅ wikipedia imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import wikipedia: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import beautifulsoup4: {e}")
        return False
    
    return True

def test_bot_import():
    """Test if the bot module can be imported"""
    print("\n🤖 Testing bot import...")
    
    try:
        from telegram_search_bot import TelegramSearchBot
        print("✅ TelegramSearchBot imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import TelegramSearchBot: {e}")
        return False
    except Exception as e:
        print(f"❌ Error importing bot: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment...")
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token:
        print("✅ TELEGRAM_BOT_TOKEN is set")
        # Don't print the actual token for security
        print(f"   Token length: {len(token)} characters")
        return True
    else:
        print("⚠️  TELEGRAM_BOT_TOKEN is not set")
        print("   This is expected if you haven't configured it yet")
        return False

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported")
        print("   Minimum required: Python 3.8")
        return False

def main():
    """Run all tests"""
    print("🧪 Telegram Search Bot - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("Module Imports", test_imports),
        ("Bot Import", test_bot_import),
        ("Environment", test_environment),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 20)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 40)
    print("📊 Test Summary")
    print("=" * 40)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("\nNext steps:")
        print("1. Set your TELEGRAM_BOT_TOKEN if not already set")
        print("2. Run: ./start_bot.sh")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check Python version: python3 --version")
        print("3. Set environment variables or create .env file")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)