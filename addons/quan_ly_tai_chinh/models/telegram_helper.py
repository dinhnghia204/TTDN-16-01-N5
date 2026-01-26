# -*- coding: utf-8 -*-
import requests
import logging

_logger = logging.getLogger(__name__)


class TelegramBot:
    """Helper class để gửi notification qua Telegram Bot"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, text, parse_mode='HTML'):
        """
        Gửi tin nhắn text qua Telegram
        
        Args:
            text (str): Nội dung tin nhắn
            parse_mode (str): 'HTML' hoặc 'Markdown'
        
        Returns:
            bool: True nếu gửi thành công
        """
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            
            # Ensure UTF-8 encoding for requests
            response = requests.post(
                url, 
                json=data, 
                timeout=5,
                headers={'Content-Type': 'application/json; charset=utf-8'}
            )
            response.raise_for_status()
            
            _logger.info(f"Telegram message sent successfully to chat {self.chat_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            _logger.error(f"Failed to send Telegram message: {str(e)}")
            return False
    
    def send_notification(self, title, message, notification_type='info'):
        """
        Gửi notification với format đẹp
        
        Args:
            title (str): Tiêu đề thông báo
            message (str): Nội dung chi tiết
            notification_type (str): 'success', 'warning', 'error', 'info'
        
        Returns:
            bool: True nếu gửi thành công
        """
        # Icon theo loại notification
        icons = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️'
        }
        
        icon = icons.get(notification_type, 'ℹ️')
        
        # Format HTML
        text = f"""
{icon} <b>{title}</b>

{message}

<i>🕐 {self._get_current_time()}</i>
"""
        
        return self.send_message(text)
    
    def _get_current_time(self):
        """Lấy thời gian hiện tại"""
        from datetime import datetime
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def get_telegram_bot(env):
    """
    Factory function để lấy TelegramBot instance từ config
    
    Args:
        env: Odoo environment
    
    Returns:
        TelegramBot or None: Instance nếu config đúng, None nếu thiếu config
    """
    try:
        # Lấy config từ System Parameters
        bot_token = env['ir.config_parameter'].sudo().get_param('telegram_bot_token')
        chat_id = env['ir.config_parameter'].sudo().get_param('telegram_chat_id')
        
        if not bot_token or not chat_id:
            _logger.warning("Telegram bot not configured. Missing bot_token or chat_id")
            return None
        
        return TelegramBot(bot_token, chat_id)
        
    except Exception as e:
        _logger.error(f"Failed to initialize Telegram bot: {str(e)}")
        return None
