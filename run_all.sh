#!/bin/bash
# Script to run both Odoo and Telegram Bot in production mode

cd "$(dirname "$0")"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting TTDN System (Odoo + Telegram Bot)...${NC}"

# 1. Kill old processes
echo -e "${YELLOW}Checking for existing processes...${NC}"
pkill -f telegram_bot_polling.py 2>/dev/null && echo -e "${GREEN}✅ Stopped old Telegram Bot${NC}"
pkill -f "odoo-bin.py" 2>/dev/null && echo -e "${GREEN}✅ Stopped old Odoo${NC}"

sleep 1

# 2. Start Telegram Bot in background
echo -e "${YELLOW}Starting Telegram Bot...${NC}"
nohup python3 addons/quan_ly_tai_chinh/telegram_bot_polling.py > telegram_bot.log 2>&1 &
BOT_PID=$!
sleep 2

if ps -p $BOT_PID > /dev/null; then
    echo -e "${GREEN}✅ Telegram Bot started (PID: $BOT_PID)${NC}"
else
    echo -e "${RED}⚠️  Telegram Bot failed to start - check telegram_bot.log${NC}"
fi

# 3. Start Odoo in background
echo -e "${YELLOW}Starting Odoo server...${NC}"
nohup python3 odoo-bin.py -c odoo.conf > odoo.log 2>&1 &
ODOO_PID=$!
sleep 3

if ps -p $ODOO_PID > /dev/null; then
    echo -e "${GREEN}✅ Odoo server started (PID: $ODOO_PID)${NC}"
else
    echo -e "${RED}⚠️  Odoo failed to start - check odoo.log${NC}"
    exit 1
fi

# 4. Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 System Started Successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}📊 Odoo:         http://localhost:8069${NC}"
echo -e "${GREEN}🤖 Telegram Bot: Running (PID: $BOT_PID)${NC}"
echo -e "${GREEN}🖥️  Odoo Server:  Running (PID: $ODOO_PID)${NC}"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  Telegram: tail -f telegram_bot.log"
echo -e "  Odoo:     tail -f odoo.log"
echo ""
echo -e "${YELLOW}Stop all:${NC}"
echo -e "  pkill -f telegram_bot_polling.py && pkill -f odoo-bin.py"
echo ""
