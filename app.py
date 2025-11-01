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

# 🎯 ПРОФЕССИОНАЛЬНАЯ СИСТЕМА INLINE-МЕНЮ (УПРОЩЕННАЯ И СТАБИЛЬНАЯ)
AI_MENUS = {
    'main': {
        'text': "🌌 *ПРИВЕТСТВУЮ, ИСКАТЕЛЬ*\n\nЯ — AI-компаньон Future_UBI. Выберите направление:",
        'keyboard': {
            "inline_keyboard": [
                [{"text": "🚀 Войти в систему AI", "callback_data": "course:ai_system"}],
                [{"text": "💫 Запустить эволюцию", "callback_data": "course:evolution"}],
                [{"text": "🌌 База знаний", "callback_data": "course:knowledge"}],
                [{"text": "⚡ Карьерный ускоритель", "callback_data": "course:career"}],
                [{"text": "💰 Премиум доступ", "callback_data": "payment:premium"}],
                [{"text": "👤 Мой профиль", "callback_data": "profile:show"}]
            ]
        }
    }
}

# 🌌 БАЗА ЗНАНИЙ ОТ СИСТЕМЫ
COURSES = {
    "🚀 Войти в систему AI": {
        "уроки": [
            "🌌 Первый контакт: основы взаимодействия с AI",
            "⚡ Когнитивное ускорение: 10x продуктивности", 
        ],
        "уровень": "🎯 Инициация в новые возможности",
        "описание": "Освойте системы, которые определяют будущее. От наблюдателя станьте творцом."
    },
    
    "💫 Запустить эволюцию": {
        "уроки": [
            "🧠 Апгрейд мышления: модели гениев",
            "🚀 Экспоненциальный рост компетенций", 
        ],
        "уровень": "🎯 Трансформация от потребителя к творцу",
        "описание": "Активируйте скрытые уровни вашего потенциала. Эволюционируйте осознанно."
    }
}

USER_PROGRESS = {}
UBI_SYSTEM = {
    "total_income": 0,
    "ubi_fund": 0,
    "distributed": 0,
    "transactions": []
}

def generate_ai_lesson(lesson_topic, user_level=1):
    """Генерирует персонализированный урок через AI"""
    try:
        prompt = f"Создай практический урок на тему: '{lesson_topic}'. Уровень сложности: {user_level}/5. Формат: теория + практическое задание."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты эксперт-преподаватель. Создавай практические уроки."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"📚 *{lesson_topic}*\n\nИзвините, в данный момент урок недоступен. Попробуйте позже."

def update_user_progress(chat_id, lesson_name):
    """Обновляет прогресс пользователя"""
    if chat_id not in USER_PROGRESS:
        USER_PROGRESS[chat_id] = {"пройденные_уроки": [], "уровень": 1, "баллы": 0}
    
    if lesson_name not in USER_PROGRESS[chat_id]["пройденные_уроки"]:
        USER_PROGRESS[chat_id]["пройденные_уроки"].append(lesson_name)
        USER_PROGRESS[chat_id]["баллы"] += 10

def generate_ton_payment_link(chat_id, amount=10):
    """Генерирует платежную ссылку для Tonkeeper"""
    return f"https://app.tonkeeper.com/transfer/UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY?amount={amount*1000000000}&text=premium_{chat_id}"

# 📍 ОСНОВНЫЕ МАРШРУТЫ
@app.route('/')
def home():
    return jsonify({
        "status": "AI Education Platform - UBI Concept",
        "version": "3.0", 
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
        
        # Обработка обычных сообщений - AI отвечает
        if 'message' in data:
            message = data['message']
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            
            if text == '/start':
                menu = AI_MENUS['main']
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": menu['text'],
                        "parse_mode": "Markdown",
                        "reply_markup": menu['keyboard']
                    }
                )
            elif text and not text.startswith('/'):
                # AI отвечает на любые сообщения
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Ты полезный AI-помощник. Отвечай понятно и по делу на русском."},
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
                        "text": f"🤖 *AI-помощник:*\n\n{ai_response}",
                        "parse_mode": "Markdown"
                    }
                )
        
        # Обработка callback запросов
        elif 'callback_query' in data:
            return callback_handler()
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/callback', methods=['POST'])
def callback_handler():
    """Обработчик callback запросов"""
    try:
        data = request.json
        callback_query = data['callback_query']
        chat_id = callback_query['message']['chat']['id']
        message_id = callback_query['message']['message_id']
        callback_data = callback_query['data']
        
        # Сразу отвечаем на callback
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
            json={"callback_query_id": callback_query['id']}
        )
        
        # 🔥 ОСНОВНЫЕ ОБРАБОТЧИКИ
        if callback_data == "menu:main":
            menu = AI_MENUS['main']
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText",
                json={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": menu['text'],
                    "reply_markup": menu['keyboard'],
                    "parse_mode": "Markdown"
                }
            )
        
        elif callback_data.startswith('course:'):
            course_id = callback_data.split(':')[1]
            course_map = {
                'ai_system': "🚀 Войти в систему AI",
                'evolution': "💫 Запустить эволюцию", 
                'knowledge': "🌌 База знаний",
                'career': "⚡ Карьерный ускоритель"
            }
            
            course_name = course_map.get(course_id)
            if course_name in COURSES:
                course_info = COURSES[course_name]
                
                lessons_keyboard = {
                    "inline_keyboard": [
                        [{"text": f"📖 {lesson}", "callback_data": f"lesson:{hash(lesson)}"}] 
                        for lesson in course_info['уроки']
                    ] + [[{"text": "◀️ На главную", "callback_data": "menu:main"}]]
                }
                
                course_text = f"*{course_name}*\n\n{course_info['описание']}\n\n*Уровень:* {course_info['уровень']}"
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText",
                    json={
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "text": course_text,
                        "reply_markup": lessons_keyboard,
                        "parse_mode": "Markdown"
                    }
                )
        
        elif callback_data.startswith('lesson:'):
            lesson_hash = callback_data.split(':')[1]
            
            for course_name, course_info in COURSES.items():
                for lesson in course_info['уроки']:
                    if str(hash(lesson)) == lesson_hash:
                        user_level = USER_PROGRESS.get(chat_id, {}).get('уровень', 1)
                        ai_lesson = generate_ai_lesson(lesson, user_level)
                        
                        lesson_keyboard = {
                            "inline_keyboard": [
                                [{"text": "✅ Завершить урок", "callback_data": f"complete:{lesson_hash}"}],
                                [{"text": "◀️ Назад", "callback_data": f"course:{course_name}"}]
                            ]
                        }
                        
                        requests.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText",
                            json={
                                "chat_id": chat_id, 
                                "message_id": message_id,
                                "text": f"📚 *{lesson}*\n\n{ai_lesson}",
                                "reply_markup": lesson_keyboard,
                                "parse_mode": "Markdown"
                            }
                        )
                        break
        
        elif callback_data.startswith('complete:'):
            lesson_hash = callback_data.replace('complete:', '')
            
            for course_name, course_info in COURSES.items():
                for lesson in course_info['уроки']:
                    if str(hash(lesson)) == lesson_hash:
                        update_user_progress(chat_id, lesson)
                        response_text = f"✅ *Урок завершен!*\n\n'{lesson}' успешно пройден.\n+10 баллов к вашему прогрессу!"
                        
                        requests.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                            json={
                                "chat_id": chat_id,
                                "text": response_text,
                                "parse_mode": "Markdown"
                            }
                        )
                        break
        
        elif callback_data == "payment:premium":
            payment_link = generate_ton_payment_link(chat_id)
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"💳 *Премиум доступ*\n\nСтоимость: 10 TON/месяц\n\n[Оплатить]({payment_link})",
                    "parse_mode": "Markdown"
                }
            )
        
        elif callback_data == "profile:show":
            progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
            response_text = f"""👤 *Ваш профиль*

📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

💫 UBI фонд: {UBI_SYSTEM['ubi_fund']} TON"""
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText",
                json={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": response_text,
                    "parse_mode": "Markdown",
                    "reply_markup": {"inline_keyboard": [[{"text": "◀️ Назад", "callback_data": "menu:main"}]]}
                }
            )
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        logging.error(f"Callback error: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/set-webhook', methods=['GET'])
def set_webhook():
    """Установка webhook для Telegram"""
    try:
        webhook_url = f"https://{request.host}/webhook"
        response = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
            params={"url": webhook_url}
        )
        return jsonify({"success": True, "webhook_url": webhook_url})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)