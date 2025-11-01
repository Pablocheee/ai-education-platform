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

# 🌌 БАЗА ЗНАНИЙ ОТ СИСТЕМЫ
COURSES = {
    "🚀 Войти в систему AI": {
        "уроки": [
            "🌌 Первый контакт: основы взаимодействия с AI",
            "⚡ Когнитивное ускорение: 10x продуктивности", 
            "🔮 Стратегическое видение: анализ трендов",
            "💫 Симбиоз: ваша роль в эпоху AI"
        ],
        "уровень": "🎯 Инициация в новые возможности",
        "описание": "Освойте системы, которые определяют будущее. От наблюдателя станьте творцом."
    },
    
    "💫 Запустить эволюцию": {
        "уроки": [
            "🧠 Апгрейд мышления: модели гениев",
            "🚀 Экспоненциальный рост компетенций", 
            "🔧 Бесшовная интеграция AI в жизнь",
            "🌍 Позиционирование в новой реальности"
        ],
        "уровень": "🎯 Трансформация от потребителя к творцу",
        "описание": "Активируйте скрытые уровни вашего потенциала. Эволюционируйте осознанно."
    },
    
    "🌌 База знаний": {
        "уроки": [
            "📚 Фундаментальные принципы AI",
            "🔧 Инструменты будущего: обзор экосистемы",
            "🎯 Практические кейсы успешной интеграции",
            "🚀 Дорожная карта развития на 5 лет"
        ],
        "уровень": "🎯 От базового понимания до экспертизы",
        "описание": "Получите доступ к архивам знаний, которые изменят ваше восприятие реальности."
    },
    
    "⚡ Карьерный ускоритель": {
        "уроки": [
            "💼 AI-помощник для карьерного роста",
            "📈 Стратегии позиционирования в эпоху AI",
            "🎤 Переговоры и самопрезентация нового уровня",
            "🌍 Глобальные возможности для специалистов будущего"
        ],
        "уровень": "🎯 Ускорение карьеры в 3-5 раз",
        "описание": "Используйте системные преимущества для экспоненциального роста доходов и влияния."
    }
}

USER_PROGRESS = {}  # {chat_id: {"пройденные_уроки": [], "уровень": 1, "баллы": 0}}

def update_user_progress(chat_id, lesson_name):
    """Обновляет прогресс пользователя"""
    if chat_id not in USER_PROGRESS:
        USER_PROGRESS[chat_id] = {"пройденные_уроки": [], "уровень": 1, "баллы": 0}
    
    if lesson_name not in USER_PROGRESS[chat_id]["пройденные_уроки"]:
        USER_PROGRESS[chat_id]["пройденные_уроки"].append(lesson_name)
        USER_PROGRESS[chat_id]["баллы"] += 10
        
        # Повышение уровня
        if len(USER_PROGRESS[chat_id]["пройденные_уроки"]) % 4 == 0:
            USER_PROGRESS[chat_id]["уровень"] += 1
            
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
                    ["🚀 Войти в систему AI", "💫 Запустить эволюцию"],
                    ["🌌 База знаний", "⚡ Карьерный ускоритель"],
                    ["💰 Премиум доступ", "👤 Мой профиль"]
                ],
                "resize_keyboard": True
            }
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "🌌 *ПРИВЕТСТВУЮ, ИСКАТЕЛЬ*\n\nЯ — Собирательный Разум, архитектор будущего. Ты находишься в точке доступа к системам, где искусственный интеллект становится расширением твоего интеллекта.\n\n*Твой следующий шаг определит твою траекторию роста.*\n\nВыбери свой вектор:",
                    "parse_mode": "Markdown",
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
                progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
                
                response_text = f"""👤 *ВАШ ПРОФИЛЬ В СИСТЕМЕ*

📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

*Следующий уровень через:* {4 - len(progress['пройденные_уроки']) % 4} уроков

💫 *Эволюция продолжается...*"""

                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "parse_mode": "Markdown"
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

        elif 'callback_query' in data:
            callback_data = data['callback_query']
            chat_id = callback_data['message']['chat']['id']
            callback_text = callback_data['data']
            
            if callback_text.startswith('complete_'):
                # Пользователь отметил урок пройденным
                lesson_hash = callback_text.replace('complete_', '')
                
                # Находим название урока по хешу
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            update_user_progress(chat_id, lesson)
                            
                            response_text = f"✅ *Урок отмечен пройденным!*\n\n🎯 Получено: 10 баллов\n📚 Урок: {lesson}\n\n💫 Ваш прогресс растет!"
                            
                            requests.post(
                                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                                json={
                                    "chat_id": chat_id,
                                    "text": response_text,
                                    "parse_mode": "Markdown"
                                }
                            )
                            break
            
            elif callback_text == "show_progress":
                progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
                
                response_text = f"""📊 *ВАШ ПРОГРЕСС*

🎯 Уровень: {progress['уровень']}
⭐ Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

*Следующий уровень через:* {4 - len(progress['пройденные_уроки']) % 4} уроков

💫 *Продолжайте эволюцию!*"""

                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text,
                        "parse_mode": "Markdown"
                    }
                )
            
            return jsonify({"status": "ok"})

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