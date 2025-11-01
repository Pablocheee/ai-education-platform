from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging

app = Flask(__name__)

# Настройка API ключей
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TON_WALLET = os.getenv('TON_WALLET', 'UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY')

@app.route('/')
def home():
    return jsonify({
        "status": "AI Education Platform - UBI Concept",
        "version": "2.0", 
        "ready": True,
        "founder_wallet": TON_WALLET
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "AI Teacher"})

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    """Webhook для Telegram бота"""
    try:
        data = request.json
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        
        if text:
            # AI ответ через OpenAI (новая версия API)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты дружелюбный AI-учитель. Объясняй понятно и интересно. Отвечай на русском."},
                    {"role": "user", "content": text}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Отправка ответа в Telegram
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id, 
                    "text": f"🎓 AI-Учитель:\n\n{ai_response}",
                    "parse_mode": "HTML"
                }
            )
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/test-ai', methods=['POST'])
def test_ai():
    """Тестовый endpoint для AI"""
    data = request.json
    user_message = data.get('message', 'Привет! Объясни что-то интересное')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты AI-преподаватель. Отвечай полезно и понятно на русском."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )
        
        return jsonify({
            "success": True,
            "response": response.choices[0].message.content
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/set-webhook', methods=['GET'])
def set_webhook():
    """Установка webhook для Telegram"""
    webhook_url = f"https://{request.host}/webhook"
    
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
            params={"url": webhook_url}
        )
        
        return jsonify({
            "success": response.status_code == 200,
            "webhook_url": webhook_url,
            "telegram_response": response.json()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)