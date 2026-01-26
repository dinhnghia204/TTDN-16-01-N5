#!/bin/bash

# Function to cleanup on exit
cleanup() {
    echo "\nStopping Telegram Bot..."
    pkill -f telegram_bot_polling.py
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT SIGTERM

# Kill old Telegram Bot if running
echo "Checking for existing Telegram Bot..."
pkill -f telegram_bot_polling.py 2>/dev/null

# Start Telegram Bot in background
echo "Starting Telegram Bot in background..."
python3 addons/quan_ly_tai_chinh/telegram_bot_polling.py > telegram_bot.log 2>&1 &
BOT_PID=$!
echo "✅ Telegram Bot started (PID: $BOT_PID)"

# Wait a moment to check if bot started successfully
sleep 2
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Telegram Bot running successfully"
else
    echo "⚠️  Telegram Bot failed to start - check telegram_bot.log"
fi

# Start Odoo (this will block until Ctrl+C)
echo "Starting Odoo server..."
python3 odoo-bin.py -c odoo.conf "$@" --dev=all

# Cleanup will run automatically when Odoo stops
