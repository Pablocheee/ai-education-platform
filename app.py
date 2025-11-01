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

UBI_SYSTEM = {
    "total_income": 0,
    "ubi_fund": 0,
    "distributed": 0,
    "transactions": []
}

# 🎯 ПРОФЕССИОНАЛЬНАЯ СИСТЕМА INLINE-МЕНЮ (ИСПРАВЛЕННАЯ)
AI_MENUS = {
    'main': {
        'text': "🌌 *ПРИВЕТСТВУЮ, ИСКАТЕЛЬ*\n\nЯ — AI-компаньон Future_UBI...",
        'keyboard': {
            "inline_keyboard": [
                [{"text": "🚀 Войти в AI-мир", "callback_data": "menu:education"}],  # ← ИСПРАВЛЕНО
                [{"text": "🎓 Начать обучение", "callback_data": "menu:education"}],
                [{"text": "💫 Моя эволюция", "callback_data": "menu:education"}],    # ← ИСПРАВЛЕНО
                [{"text": "⚡ Ускорить карьеру", "callback_data": "menu:education"}], # ← ИСПРАВЛЕНО
                [{"text": "👤 Мой профиль", "callback_data": "profile:show"}]        # ← ДОБАВЛЕНО
            ]
        }
    },
    
    'education': {
        'text': "🎓 *ВЫБЕРИТЕ НАПРАВЛЕНИЕ ОБУЧЕНИЯ*\n\nКаждый курс адаптируется под ваш стиль и темп.",
        'keyboard': {
            "inline_keyboard": [
                [{"text": "🚀 Войти в систему AI", "callback_data": "course:ai_system"}],
                [{"text": "💫 Запустить эволюцию", "callback_data": "course:evolution"}],
                [{"text": "🌌 База знаний", "callback_data": "course:knowledge"}],
                [{"text": "⚡ Карьерный ускоритель", "callback_data": "course:career"}],
                [{"text": "💰 Премиум доступ", "callback_data": "menu:premium"}],
                [{"text": "◀️ На главную", "callback_data": "menu:main"}]
            ]
        }
    },
    
    'premium': {
        'text': "💰 *ПРЕМИУМ ДОСТУП*\n\nПолучите полную мощь AI-обучения 24/7",
        'keyboard': {
            "inline_keyboard": [
                [{"text": "💳 Оплатить 10 TON", "callback_data": "payment:premium"}],
                [{"text": "🎓 Все курсы", "callback_data": "menu:education"}],
                [{"text": "◀️ На главную", "callback_data": "menu:main"}]
            ]
        }
    }
}

def generate_ai_lesson(lesson_topic, user_level=1):
    """Генерирует персонализированный урок через AI"""
    prompt = f"""
    Создай образовательный контент на тему: "{lesson_topic}"
    
    Требования:
    - Уровень сложности: {user_level}/5
    - Формат: практический урок с примерами
    - Структура: теория + практическое задание
    - Длина: 500-700 слов
    - Язык: русский с профессиональной лексикой
    
    Содержание:
    1. Ключевая концепция (простыми словами)
    2. Практические примеры из реальной жизни  
    3. Пошаговое руководство по применению
    4. Задание для закрепления
    5. Советы для дальнейшего развития
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты эксперт-преподаватель с 20-летним опытом. Создавай практические, полезные уроки которые сразу можно применять в работе."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    
    return response.choices[0].message.content

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

def process_ubi_payment(amount, from_user):
    """Обрабатывает платеж и распределяет по UBI"""
    UBI_SYSTEM["total_income"] += amount
    
    distribution = {
        "reinvestment": amount * 0.6,      # 60% на развитие
        "ubi_fund": amount * 0.3,          # 30% в UBI фонд  
        "founder": amount * 0.1            # 10% основателю
    }
    
    UBI_SYSTEM["ubi_fund"] += distribution["ubi_fund"]  # ← ОБНОВЛЯЕМ ФОНД
    UBI_SYSTEM["distributed"] += distribution["ubi_fund"]
    UBI_SYSTEM["transactions"].append({
        "amount": amount,
        "from": from_user,
        "distribution": distribution,
        "timestamp": "2025-01-11"
    })
    
    return distribution

def generate_ai_lesson(lesson_topic, user_level=1):
    """Генерирует персонализированный урок через AI"""
    prompt = f"""
    Создай образовательный контент на тему: "{lesson_topic}"
    
    Требования:
    - Уровень сложности: {user_level}/5
    - Формат: практический урок с примерами
    - Структура: теория + практическое задание
    - Длина: 500-700 слов
    - Язык: русский с профессиональной лексикой
    
    Содержание:
    1. Ключевая концепция (простыми словами)
    2. Практические примеры из реальной жизни  
    3. Пошаговое руководство по применению
    4. Задание для закрепления
    5. Советы для дальнейшего развития
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты эксперт-преподаватель с 20-летним опытом. Создавай практические, полезные уроки которые сразу можно применять в работе."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    
    return response.choices[0].message.content
            
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
        
        # Обработка callback_query (inline-кнопки)
        if 'callback_query' in data:
            # ✅ Сохраняем результат callback_handler и возвращаем его
            result = callback_handler()
            return result
            
        message = data.get('message', {})
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
        
        # ✅ Всегда возвращаем response
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
        # Тестовая реализация - при первом платеже добавляем 10 TON
        if UBI_SYSTEM["total_income"] == 0:
            distribution = process_ubi_payment(10, "first_payment")
            return jsonify({
                "status": "success", 
                "distribution": distribution,
                "message": f"💰 Первый доход! UBI фонд пополнен на {distribution['ubi_fund']} TON"
            })
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

@app.route('/callback', methods=['POST'])
def callback_handler():
    """Обработчик ВСЕХ callback запросов от кнопок"""
    try:
        data = request.json
        callback_query = data['callback_query']
        chat_id = callback_query['message']['chat']['id']
        message_id = callback_query['message']['message_id']
        callback_data = callback_query['data']
        
        print(f"DEBUG: Получен callback_data: {callback_data}")
        
        # Сразу отвечаем на callback чтобы убрать часики
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
            json={"callback_query_id": callback_query['id']}
        )
        
        # 🔥 ОБРАБОТКА МЕНЮ
        if callback_data.startswith('menu:'):
            menu_name = callback_data.split(':')[1]
            menu = AI_MENUS.get(menu_name, AI_MENUS['main'])
            
            print(f"DEBUG: Открываем меню: {menu_name}")
            
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
        
        # 🔥 ОБРАБОТКА КУРСОВ
        elif callback_data.startswith('course:'):
            course_id = callback_data.split(':')[1]
            course_map = {
                'ai_system': "🚀 Войти в систему AI",
                'evolution': "💫 Запустить эволюцию", 
                'knowledge': "🌌 База знаний",
                'career': "⚡ Карьерный ускоритель"
            }
            
            course_name = course_map.get(course_id)
            if course_name and course_name in COURSES:
                course_info = COURSES[course_name]
                
                lessons_keyboard = {
                    "inline_keyboard": [
                        [{"text": f"📖 {lesson}", "callback_data": f"lesson:{hash(lesson)}"}] 
                        for lesson in course_info['уроки']
                    ] + [[{"text": "◀️ Назад к курсам", "callback_data": "menu:education"}]]
                }
                
                course_text = f"*{course_name}*\n\n{course_info['описание']}\n\n*Уровень:* {course_info['уровень']}\n\n*Доступные уроки:*"
                
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
        
        # 🔥 ОБРАБОТКА УРОКОВ
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
                                [{"text": "◀️ Назад к курсу", "callback_data": f"course:{course_name}"}]
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
        
        # 🔥 ОБРАБОТКА ЗАВЕРШЕНИЯ УРОКОВ
        elif callback_data.startswith('complete:'):
            lesson_hash = callback_data.replace('complete:', '')
            
            for course_name, course_info in COURSES.items():
                for lesson in course_info['уроки']:
                    if str(hash(lesson)) == lesson_hash:
                        update_user_progress(chat_id, lesson)
                        
                        completion_responses = [
                            f"🌌 *АКТИВАЦИЯ НЕЙРОННОЙ СЕТИ*\n\nУрок '{lesson}' интегрирован в твое сознание.\n\n+10 единиц когнитивной мощности\n💫 Твой путь к кибернетическому существованию продолжается...",
                            f"⚡ *СИНАПСИЧЕСКОЕ СОЕДИНЕНИЕ УСТАНОВЛЕНО*\n\n'{lesson}' теперь часть твоего ментального арсенаала.\n\n🎯 Уровень понимания повышен\n🔮 Новые паттерны доступны для анализа...",
                        ]
                        
                        import random
                        response_text = random.choice(completion_responses)
                        
                        requests.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                            json={
                                "chat_id": chat_id,
                                "text": response_text,
                                "parse_mode": "Markdown"
                            }
                        )
                        break
        
        # 🔥 ОБРАБОТКА ПЛАТЕЖЕЙ
        elif callback_data == "payment:premium":
            payment_link = generate_ton_payment_link(chat_id)
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"💳 *ОПЛАТА ПРЕМИУМ ДОСТУПА*\n\nСтоимость: 10 TON/месяц\n\n[Оплатить]({payment_link})",
                    "parse_mode": "Markdown"
                }
            )

        # 🔥 ОБРАБОТКА ПРОФИЛЯ
        elif callback_data == "profile:show":
            progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
            
            response_text = f"""👤 *ВАШ ПРОФИЛЬ В СИСТЕМЕ*

📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

🌍 *UBI СИСТЕМА*
💫 Собрано в фонд: {UBI_SYSTEM['ubi_fund']} TON
🚀 Всего доходов: {UBI_SYSTEM['total_income']} TON"""

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

        # ✅ ВАЖНО: Всегда возвращаем response
        return jsonify({"status": "processing"})
        
    except Exception as e:
        logging.error(f"Callback error: {e}")
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
            params={
                "url": webhook_url,
                "allowed_updates": ["message", "callback_query"]
            }
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