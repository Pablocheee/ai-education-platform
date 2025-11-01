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

# 🎓 СТРУКТУРА КУРСОВ FUTURE_UBI
COURSES = {
    "🧮 Математика": {
        "уроки": [
            "➗ Арифметика: основы счета", 
            "📐 Геометрия: фигуры и пространство",
            "📊 Алгебра: переменные и уравнения",
            "📈 Матанализ: производные и интегралы"
        ],
        "уровень": "🎯 От начального до продвинутого",
        "описание": "Освойте язык вселенной через практические задачи и AI-объяснения"
    },
    
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Английский": {
        "уроки": [
            "🔤 Базовый английский: алфавит и простые фразы",
            "📝 Грамматика: времена и конструкции", 
            "🗣️ Разговорная практика с AI-носителем",
            "💼 Бизнес английский: переговоры и презентации"
        ],
        "уровень": "🎯 Уровни A1-C2",
        "описание": "Станьте полиглотом с персональным AI-преподавателем 24/7"
    },
    
    "💻 Программирование": {
        "уроки": [
            "🐍 Python: синтаксис и основы",
            "⚙️ Функции, классы и ООП",
            "🌐 Web разработка: Flask и API",
            "🧠 AI и машинное обучение"
        ],
        "уровень": "🎯 С нуля до Junior Developer",
        "описание": "Создавайте AI-приложения и автоматизируйте мир вокруг себя"
    }
}

def generate_ton_payment_link(chat_id, amount=10):
    """Генерирует платежную ссылку для Tonkeeper"""
    return f"https://app.tonkeeper.com/transfer/UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY?amount={amount*1000000000}&text=premium_{chat_id}"

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

        # Обработка команды /start - показываем меню с кнопками
        if text == '/start':
            keyboard = {
                "keyboard": [
                    ["🎓 Бесплатные уроки", "💰 Премиум подписка"],
                    ["👤 Мой профиль", "ℹ️ О проекте"]
                ],
                "resize_keyboard": True
            }
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "🤖 Добро пожаловать в AI-школу Future_UBI!\n\nВыберите действие:",
                    "reply_markup": keyboard
                }
            )
            return jsonify({"status": "ok"})

        # Обработка нажатий кнопок
        elif text in ["🎓 Бесплатные уроки", "💰 Премиум подписка", "👤 Мой профиль", "ℹ️ О проекте"]:
            if text == "🎓 Бесплатные уроки":
                # Создаем клавиатуру с курсами
                keyboard = {
                    "keyboard": [
                        ["🧮 Математика", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Английский"],
                        ["💻 Программирование", "👤 Мой профиль"]
                    ],
                    "resize_keyboard": True
                }
                
                response_text = "🎓 Выберите курс для изучения:\n\nКаждый курс включает:\n• Практические уроки\n• AI-преподаватель 24/7\n• Прогресс обучения"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "reply_markup": keyboard
                    }
                )
                
            elif text == "💰 Премиум подписка":
                # Генерируем реальную платежную ссылку
                payment_link = generate_ton_payment_link(chat_id)
                
                # Создаем инлайн-кнопку для оплаты
                inline_keyboard = {
                    "inline_keyboard": [[
                        {
                            "text": "💳 Оплатить 10 TON", 
                            "url": payment_link
                        }
                    ]]
                }
                
                response_text = "💰 Премиум подписка\n\n✅ Полный доступ ко всем курсам\n🎓 Персональный AI-учитель 24/7\n📊 Прогресс обучения и сертификаты\n\nСтоимость: 10 TON/месяц"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "reply_markup": inline_keyboard,
                        "parse_mode": "HTML"
                    }
                )

            elif text == "🧮 Математика":
                course_info = COURSES["🧮 Математика"]
                response_text = f"🧮 Математика\n\n{course_info['описание']}\n\nУровень: {course_info['уровень']}\n\nУроки:\n" + "\n".join([f"• {lesson}" for lesson in course_info['уроки']])
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "parse_mode": "HTML"
                    }
                )

            elif text == "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Английский":
                course_info = COURSES["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Английский"]
                response_text = f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 Английский\n\n{course_info['описание']}\n\nУровень: {course_info['уровень']}\n\nУроки:\n" + "\n".join([f"• {lesson}" for lesson in course_info['уроки']])
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "parse_mode": "HTML"
                    }
                )

            elif text == "💻 Программирование":
                course_info = COURSES["💻 Программирование"]
                response_text = f"💻 Программирование\n\n{course_info['описание']}\n\nУровень: {course_info['уровень']}\n\nУроки:\n" + "\n".join([f"• {lesson}" for lesson in course_info['уроки']])
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "parse_mode": "HTML"
                    }
                )
                    
            elif text == "👤 Мой профиль":
                response_text = f"👤 Ваш профиль:\n\nID: {chat_id}\nСтатус: Бесплатный аккаунт\nПрогресс: 0 уроков пройдено\n\nПерейдите на премиум для полного доступа!"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "parse_mode": "HTML"
                    }
                )
                
            else:  # ℹ️ О проекте
                response_text = "ℹ️ Future_UBI - автономная AI-компания\n\nМиссия: Люди творят, AI работает, UBI распределяет\n\n60% - развитие платформы\n30% - универсальный базовый доход\n10% - основателю"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "parse_mode": "HTML"
                    }
                )
            
            return jsonify({"status": "ok"})

        # Обычные сообщения - обрабатываем AI
        elif text:
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

TON_API_KEY = "AEZIWI7NPO6LFRIAAAAFCRWL76ZY7YKGQS2HFKW66VUFXS4NR2M54PJL2NJBUYWDWFX4BEQ"

@app.route('/ton-payment-webhook', methods=['POST'])
def ton_payment_webhook():
    """Вебхук для подтверждения платежей TON"""
    try:
        data = request.json
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"})

@app.route('/setup-ton-webhook', methods=['GET'])
def setup_ton_webhook():
    """Настройка вебхука в TON API"""
    try:
        webhook_url = f"https://{request.host}/ton-payment-webhook"
        
        response = requests.post(
            "https://rt.tonapi.io/webhooks",
            headers={"Authorization": f"Bearer {TON_API_KEY}"},
            json={
                "endpoint": webhook_url
            }
        )
        
        return jsonify({
            "success": response.status_code == 200,
            "webhook_url": webhook_url,
            "response": response.json()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/subscribe-wallet', methods=['GET'])
def subscribe_wallet():
    """Подписка вебхука на кошелек для отслеживания платежей"""
    try:
        response = requests.post(
            "https://rt.tonapi.io/webhooks/15412/account-tx/subscribe",
            headers={"Authorization": f"Bearer {TON_API_KEY}"},
            json={
                "accounts": [{
                    "account_id": "UQAbs4Ak99raDhS8FUWLWNvKoUQ1LiHIxndfiIAj8p9BiusC"
                }]
            }
        )
        
        return jsonify({
            "success": response.status_code == 200,
            "response": response.json()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

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