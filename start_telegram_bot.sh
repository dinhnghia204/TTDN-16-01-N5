#!/bin/bash
# Script to start Telegram bot polling service

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run polling bot
echo "Starting Telegram bot polling service..."
python3 addons/quan_ly_tai_chinh/telegram_bot_polling.py
