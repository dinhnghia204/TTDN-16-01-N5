#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot Polling Service
Chạy service này để bot lắng nghe và xử lý tin nhắn từ Telegram
"""

import sys
import os
import time
import logging
import requests

# Add Odoo to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import odoo
from odoo import api, SUPERUSER_ID

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('telegram_bot_polling')


class TelegramBotPolling:
    def __init__(self, bot_token, chat_id, dbname='odoo'):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.dbname = dbname
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.last_update_id = 0
        
    def get_updates(self, timeout=30):
        """Lấy tin nhắn mới từ Telegram"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {
                'offset': self.last_update_id + 1,
                'timeout': timeout,
                'allowed_updates': ['message']
            }
            response = requests.get(url, params=params, timeout=timeout+5)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    return data.get('result', [])
                else:
                    logger.error(f"Telegram API error: {data}")
            else:
                logger.error(f"HTTP error {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            logger.debug("Timeout waiting for updates (normal)")
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
        return []
    
    def send_message(self, text, parse_mode='HTML'):
        """Gửi tin nhắn đến Telegram"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text
            }
            if parse_mode:
                data['parse_mode'] = parse_mode
                
            response = requests.post(
                url,
                json=data,
                headers={'Content-Type': 'application/json; charset=utf-8'}
            )
            if response.status_code == 200:
                logger.info(f"Message sent to Telegram")
                return True
            else:
                logger.error(f"Failed to send message: {response.text}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
        return False
    
    def process_message(self, message):
        """Xử lý tin nhắn từ Telegram"""
        try:
            # Extract message info
            message_id = message.get('message_id')
            chat = message.get('chat', {})
            msg_chat_id = str(chat.get('id', ''))
            text = message.get('text', '').strip()
            from_user = message.get('from', {})
            user_name = from_user.get('first_name', 'Unknown')
            
            logger.info(f"Processing message {message_id} from {user_name}: {text}")
            
            # Verify chat_id
            if msg_chat_id != str(self.chat_id):
                logger.warning(f"Ignored message from unauthorized chat: {msg_chat_id}")
                return
            
            # Process command with Odoo
            with odoo.api.Environment.manage():
                registry = odoo.registry(self.dbname)
                with registry.cursor() as cr:
                    env = api.Environment(cr, SUPERUSER_ID, {})
                    
                    # Call command handler
                    CommandHandler = env['telegram.command.handler']
                    response = CommandHandler.handle_command(text, msg_chat_id, user_name)
                    
                    # Send response (use plain text for commands with formatting issues)
                    if response:
                        parse_mode = None if '/help' in text else 'HTML'
                        self.send_message(response, parse_mode=parse_mode)
                    
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            self.send_message(f"❌ Lỗi xử lý lệnh: {str(e)}")
    
    def run(self):
        """Chạy bot polling loop"""
        logger.info(f"Starting Telegram bot polling for chat {self.chat_id}")
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        try:
            while True:
                updates = self.get_updates()
                
                if updates:
                    for update in updates:
                        # Update last_update_id
                        update_id = update.get('update_id')
                        if update_id > self.last_update_id:
                            self.last_update_id = update_id
                        
                        # Process message if exists
                        message = update.get('message')
                        if message:
                            self.process_message(message)
                
                # Small delay to prevent busy loop
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("\nStopping bot...")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)


def main():
    """Main entry point"""
    # Configuration
    BOT_TOKEN = "8573098191:AAH1dVCI5uRqR0_fdPbt5b3abvraJ7Lo3wY"
    CHAT_ID = "8082274502"
    DBNAME = "odoo"
    
    # Initialize Odoo
    config_file = '/home/nghiax/TTDN-16-01-N5/odoo.conf'
    
    if not os.path.exists(config_file):
        logger.error(f"Config file not found: {config_file}")
        sys.exit(1)
    
    odoo.tools.config.parse_config(['-c', config_file])
    
    # Create and run bot
    bot = TelegramBotPolling(BOT_TOKEN, CHAT_ID, DBNAME)
    bot.run()


if __name__ == '__main__':
    main()
