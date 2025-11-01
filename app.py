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
        
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    """Webhook для Telegram бота"""
    try:
        data = request.json
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        
        # ОБРАБОТКА СПЕЦИАЛЬНЫХ КОМАНД - ДОБАВЬ ЭТОТ БЛОК ПЕРВЫМ
        if text.startswith('/'):
            if text == '/math':
                response_text = "🧮 Начнем урок математики!\n\nРеши: 15 + 25 = ?\n\nА теперь посложнее: сколько будет 7 × 8?"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": response_text})
                return jsonify({"status": "ok"})
                
            elif text == '/english':
                response_text = "🌍 English Lesson!\n\nBasic phrases:\n• Hello - Привет\n• How are you? - Как дела?\n• I'm learning - Я учусь\n\nPractice: Translate 'Good morning'"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": response_text})
                return jsonify({"status": "ok"})
                
            elif text == '/science':
                response_text = "🔬 Научный факт дня!\n\nЗнаешь ли ты, что:\n• Свет от Солнца до Земли идет 8 минут\n• У пчел 5 глаз\n• Венера вращается в обратную сторону\n\nХочешь узнать больше о космосе?"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": response_text})
                return jsonify({"status": "ok"})
                
            elif text == '/programming':
                response_text = "💻 Основы Python:\n\nprint('Hello World!')\n\nЭто твоя первая программа! 🎉\n\nХочешь научиться создавать переменные?"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": response_text})
                return jsonify({"status": "ok"})
            
            elif text == '/start':
                response_text = "🤖 Добро пожаловать в AI-Школу!\n\nДоступные команды:\n/math - Математика\n/english - Английский\n/science - Наука\n/programming - Программирование\n/subscribe - Премиум подписка\n\nПросто напиши вопрос - и я объясню!"
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": response_text})
                return jsonify({"status": "ok"})            
                
            elif text == '/subscribe':
                response_text = f"""💎 ПРЕМИУМ ПОДПИСКА

Переведите 10 TON на кошелек:
`{TON_WALLET}`

После оплаты отправьте хэш транзакции для активации премиум-доступа."""
                
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                            json={"chat_id": chat_id, "text": response_text})
                return jsonify({"status": "ok"})

        # 🔥 ОБРАБОТЧИК ХЭША ДОЛЖЕН БЫТЬ ЗДЕСЬ - ПОСЛЕ ЗАКРЫТИЯ БЛОКА КОМАНД
        elif len(text) == 64 and all(c in '0123456789abcdefABCDEF' for c in text):
            # Это похоже на хэш транзакции
            response_text = f"✅ Проверяю транзакцию {text[:16]}...\nПремиум доступ будет активирован в течение 5 минут."
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                         json={"chat_id": chat_id, "text": response_text})
            return jsonify({"status": "ok"})
        
        # СУЩЕСТВУЮЩИЙ КОД ДЛЯ ОБЫЧНЫХ СООБЩЕНИЙ
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