# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)


class TelegramWebhook(http.Controller):
    """Controller để nhận webhook từ Telegram"""
    
    @http.route('/telegram/webhook', type='json', auth='none', methods=['POST'], csrf=False)
    def telegram_webhook(self, **kwargs):
        """
        Nhận tin nhắn từ Telegram bot
        
        Telegram sẽ gửi POST request khi user gửi tin nhắn:
        {
            "update_id": 123456789,
            "message": {
                "message_id": 1,
                "from": {"id": 8082274502, "first_name": "Nghia"},
                "chat": {"id": 8082274502, "type": "private"},
                "text": "/start"
            }
        }
        """
        try:
            # Parse request data
            data = json.loads(request.httprequest.data)
            _logger.info(f"Received Telegram webhook: {data}")
            
            # Extract message info
            if 'message' not in data:
                return {'ok': True, 'message': 'No message'}
            
            message = data['message']
            chat_id = str(message['chat']['id'])
            text = message.get('text', '')
            user_name = message['from'].get('first_name', 'User')
            
            # Verify chat_id matches config
            bot_chat_id = request.env['ir.config_parameter'].sudo().get_param('telegram_chat_id')
            if chat_id != bot_chat_id:
                _logger.warning(f"Unauthorized chat_id: {chat_id}")
                return {'ok': False, 'message': 'Unauthorized'}
            
            # Handle command
            command_handler = request.env['telegram.command.handler'].sudo()
            response = command_handler.handle_command(text, chat_id, user_name)
            
            # Send response back to user
            from odoo.addons.quan_ly_tai_chinh.models.telegram_helper import get_telegram_bot
            telegram_bot = get_telegram_bot(request.env)
            if telegram_bot:
                telegram_bot.send_message(response, parse_mode='HTML')
            
            return {'ok': True, 'message': 'Processed'}
            
        except Exception as e:
            _logger.error(f"Error processing Telegram webhook: {str(e)}")
            return {'ok': False, 'error': str(e)}
    
    @http.route('/telegram/set_webhook', type='http', auth='user', methods=['GET'])
    def set_webhook(self, **kwargs):
        """
        Setup webhook URL for Telegram bot
        Call: http://localhost:8069/telegram/set_webhook
        """
        try:
            # Get bot token
            bot_token = request.env['ir.config_parameter'].sudo().get_param('telegram_bot_token')
            if not bot_token:
                return "Error: telegram_bot_token not configured"
            
            # Get base URL
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            webhook_url = f"{base_url}/telegram/webhook"
            
            # Set webhook via Telegram API
            import requests
            api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
            response = requests.post(api_url, json={'url': webhook_url})
            
            result = response.json()
            if result.get('ok'):
                return f"✅ Webhook set successfully!\n\nURL: {webhook_url}\n\nResult: {json.dumps(result, indent=2)}"
            else:
                return f"❌ Failed to set webhook\n\nResult: {json.dumps(result, indent=2)}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    @http.route('/telegram/webhook_info', type='http', auth='user', methods=['GET'])
    def webhook_info(self, **kwargs):
        """
        Kiểm tra webhook status
        Call: http://localhost:8069/telegram/webhook_info
        """
        try:
            bot_token = request.env['ir.config_parameter'].sudo().get_param('telegram_bot_token')
            if not bot_token:
                return "Error: telegram_bot_token not configured"
            
            import requests
            api_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
            response = requests.get(api_url)
            
            result = response.json()
            return f"<pre>{json.dumps(result, indent=2)}</pre>"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    @http.route('/telegram/delete_webhook', type='http', auth='user', methods=['GET'])
    def delete_webhook(self, **kwargs):
        """
        Xóa webhook (chuyển về polling mode)
        Call: http://localhost:8069/telegram/delete_webhook
        """
        try:
            bot_token = request.env['ir.config_parameter'].sudo().get_param('telegram_bot_token')
            if not bot_token:
                return "Error: telegram_bot_token not configured"
            
            import requests
            api_url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
            response = requests.post(api_url)
            
            result = response.json()
            if result.get('ok'):
                return "✅ Webhook deleted successfully! Bot is now in polling mode."
            else:
                return f"❌ Failed to delete webhook\n\nResult: {json.dumps(result, indent=2)}"
                
        except Exception as e:
            return f"Error: {str(e)}"
