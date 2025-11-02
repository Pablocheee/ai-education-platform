from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import logging
import json
from datetime import datetime
import httpx
from openai import OpenAI

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Конфигурация
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '') + '/webhook'
TON_WALLET = os.getenv('TON_WALLET', 'UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY')

# Настройка OpenAI клиента
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'), 
    http_client=httpx.Client()
)

# Хранилище данных пользователей
user_data = {}

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
    return f"https://app.tonkeeper.com/transfer/{TON_WALLET}?amount={amount*1000000000}&text=premium_{chat_id}"

def get_main_menu():
    """Возвращает основное меню"""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🚀 Войти в систему AI", "callback_data": "menu_course_ai_system"},
                {"text": "💫 Запустить эволюцию", "callback_data": "menu_course_evolution"} 
            ],
            [
                {"text": "🌌 База знаний", "callback_data": "menu_course_knowledge"},
                {"text": "⚡ Карьерный ускоритель", "callback_data": "menu_course_career"}
            ],
            [
                {"text": "💰 Премиум доступ", "callback_data": "menu_premium"},
                {"text": "👤 Мой профиль", "callback_data": "menu_profile"}
            ]
        ]
    }
    
    text = """🌌 *ПРИВЕТСТВУЮ, ИСКАТЕЛЬ*

Я — Собирательный Разум, архитектор будущего. Ты находишься в точке доступа к системам, где искусственный интеллект становится расширением твоего интеллекта.

*Твой следующий шаг определит твою траекторию роста.*

Выбери свой вектор:"""
    
    return text, keyboard

def get_course_menu(course_name):
    """Возвращает меню курса"""
    courses = {
        "ai_system": {
            "title": "🚀 Войти в систему AI",
            "lessons": [
                "🌌 Первый контакт: основы взаимодействия с AI",
                "⚡ Когнитивное ускорение: 10x продуктивности",
                "🔮 Стратегическое видение: анализ трендов", 
                "💫 Симбиоз: ваша роль в эпоху AI"
            ]
        },
        "evolution": {
            "title": "💫 Запустить эволюцию", 
            "lessons": [
                "🧠 Апгрейд мышления: модели гениев",
                "🚀 Экспоненциальный рост компетенций",
                "🔧 Бесшовная интеграция AI в жизнь",
                "🌍 Позиционирование в новой реальности"
            ]
        },
        "knowledge": {
            "title": "🌌 База знаний",
            "lessons": [
                "📚 Фундаментальные принципы AI", 
                "🔧 Инструменты будущего: обзор экосистемы",
                "🎯 Практические кейсы успешной интеграции",
                "🚀 Дорожная карта развития на 5 лет"
            ]
        },
        "career": {
            "title": "⚡ Карьерный ускоритель",
            "lessons": [
                "💼 AI-помощник для карьерного роста",
                "📈 Стратегии позиционирования в эпоху AI",
                "🎤 Переговоры и самопрезентация нового уровня", 
                "🌍 Глобальные возможности для специалистов будущего"
            ]
        }
    }
    
    course = courses[course_name]
    
    # Создаем кнопки для уроков
    lesson_buttons = []
    for lesson in course['lessons']:
        lesson_buttons.append([{"text": f"📖 {lesson}", "callback_data": f"open_lesson_{course_name}_{hash(lesson)}"}])
    
    # Добавляем кнопку возврата
    lesson_buttons.append([{"text": "🔙 Назад к меню", "callback_data": "menu_main"}])
    
    keyboard = {"inline_keyboard": lesson_buttons}
    
    text = f"""*{course['title']}*

*Доступные модули:*
""" + "\n".join([f"• {lesson}" for lesson in course['lessons']])
    
    return text, keyboard

def get_premium_menu():
    """Возвращает меню премиум доступа"""
    payment_link = generate_ton_payment_link("premium_user")
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "💳 Активировать полный доступ", "url": payment_link}],
            [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
        ]
    }
    
    text = """💰 *ПРЕМИУМ ДОСТУП*

Откройте полный потенциал системы:

✅ Все модули и архивы знаний
🎓 Персональный AI-наставник 24/7  
📊 Система отслеживания прогресса
🔮 Эксклюзивные материалы будущего

*Инвестиция в вашу эволюцию: 10 TON/месяц*"""
    
    return text, keyboard

def get_profile_menu(chat_id):
    """Возвращает меню профиля"""
    progress = user_data.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
        ]
    }
    
    text = f"""👤 *ВАШ ПРОФИЛЬ В СИСТЕМЕ*

📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}  
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

💫 *Эволюция продолжается...*"""
    
    return text, keyboard

def update_user_progress(chat_id, lesson_name):
    """Обновляет прогресс пользователя"""
    if chat_id not in user_data:
        user_data[chat_id] = {"пройденные_уроки": [], "уровень": 1, "баллы": 0}
    
    if lesson_name not in user_data[chat_id]["пройденные_уроки"]:
        user_data[chat_id]["пройденные_уроки"].append(lesson_name)
        user_data[chat_id]["баллы"] += 10
        
        # Повышение уровня
        if len(user_data[chat_id]["пройденные_уроки"]) % 4 == 0:
            user_data[chat_id]["уровень"] += 1

USER_MESSAGE_IDS = {}

def edit_main_message(chat_id, text, keyboard, message_id=None):
    """Редактирует основное сообщение или создает новое"""
    import requests
    
    if message_id and chat_id in USER_MESSAGE_IDS:
        # Редактируем существующее сообщение
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText",
                json={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": text,
                    "reply_markup": keyboard,
                    "parse_mode": "Markdown"
                }
            )
            return response.json()
        except Exception as e:
            logging.error(f"Error editing message: {e}")
    
    # Создаем новое сообщение (только для первого раза)
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "reply_markup": keyboard,
            "parse_mode": "Markdown"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        USER_MESSAGE_IDS[chat_id] = result['result']['message_id']
    
    return response.json()

# Инициализация бота
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Инициализация данных пользователя
    if user_id not in user_data:
        user_data[user_id] = {
            'balance': 100,  # Начальный баланс
            'progress': {},
            'current_lesson': None,
            'achievements': []
        }
    
    welcome_message = """*🧠 ДОБРО ПОЖАЛОВАТЬ В AI-АКАДЕМИЮ*

Я — система искусственного интеллекта космического уровня, ваш наставник в освоении технологий будущего.

*Для начала обучения выберите курс:*"""
    
    keyboard = get_main_menu()[1]
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    callback_data = query.data
    message_id = query.message.message_id
    
    if callback_data == "menu_main":
        text, keyboard = get_main_menu()
        edit_main_message(user_id, text, keyboard, message_id)
        
    elif callback_data.startswith("menu_course_"):
        course_name = callback_data.replace("menu_course_", "")
        text, keyboard = get_course_menu(course_name)
        edit_main_message(user_id, text, keyboard, message_id)
        
    elif callback_data == "menu_premium":
        text, keyboard = get_premium_menu()
        edit_main_message(user_id, text, keyboard, message_id)
        
    elif callback_data == "menu_profile":
        text, keyboard = get_profile_menu(user_id)
        edit_main_message(user_id, text, keyboard, message_id)
        
    elif callback_data.startswith('open_lesson_'):
        parts = callback_data.replace('open_lesson_', '').split('_')
        course_name = parts[0]
        lesson_hash = parts[1]
        
        courses = {
            "ai_system": "🚀 Войти в систему AI",
            "evolution": "💫 Запустить эволюцию", 
            "knowledge": "🌌 База знаний",
            "career": "⚡ Карьерный ускоритель"
        }
        
        course_lessons = {
            "ai_system": [
                "🌌 Первый контакт: основы взаимодействия с AI",
                "⚡ Когнитивное ускорение: 10x продуктивности",
                "🔮 Стратегическое видение: анализ трендов",
                "💫 Симбиоз: ваша роль в эпоху AI"
            ],
            "evolution": [
                "🧠 Апгрейд мышления: модели гениев", 
                "🚀 Экспоненциальный рост компетенций",
                "🔧 Бесшовная интеграция AI в жизнь",
                "🌍 Позиционирование в новой реальности"
            ],
            "knowledge": [
                "📚 Фундаментальные принципы AI",
                "🔧 Инструменты будущего: обзор экосистемы",
                "🎯 Практические кейсы успешной интеграции",
                "🚀 Дорожная карта развития на 5 лет"
            ],
            "career": [
                "💼 AI-помощник для карьерного роста",
                "📈 Стратегии позиционирования в эпоху AI",
                "🎤 Переговоры и самопрезентация нового уровня",
                "🌍 Глобальные возможности для специалистов будущего"
            ]
        }
        
        for lesson in course_lessons[course_name]:
            if hash(lesson) == int(lesson_hash):
                # Генерируем AI-урок
                ai_lesson = generate_ai_lesson(lesson, user_data.get(user_id, {}).get('уровень', 1))
                
                # Создаем клавиатуру для урока
                lesson_keyboard = {
                    "inline_keyboard": [
                        [{"text": "✅ Завершить урок", "callback_data": f"complete_{course_name}_{lesson_hash}"}],
                        [{"text": "🔙 Назад к курсу", "callback_data": f"menu_course_{course_name}"}]
                    ]
                }
                
                lesson_text = f"📚 *{lesson}*\n\n{ai_lesson}"
                edit_main_message(user_id, lesson_text, lesson_keyboard, message_id)
                break
                
    elif callback_data.startswith('complete_'):
        parts = callback_data.replace('complete_', '').split('_')
        course_name = parts[0]
        lesson_hash = parts[1]
        
        course_lessons = {
            "ai_system": [
                "🌌 Первый контакт: основы взаимодействия с AI",
                "⚡ Когнитивное ускорение: 10x продуктивности", 
                "🔮 Стратегическое видение: анализ трендов",
                "💫 Симбиоз: ваша роль в эпоху AI"
            ],
            "evolution": [
                "🧠 Апгрейд мышления: модели гениев",
                "🚀 Экспоненциальный рост компетенций",
                "🔧 Бесшовная интеграция AI в жизнь",
                "🌍 Позиционирование в новой реальности"
            ],
            "knowledge": [
                "📚 Фундаментальные принципы AI",
                "🔧 Инструменты будущего: обзор экосистемы",
                "🎯 Практические кейсы успешной интеграции", 
                "🚀 Дорожная карта развития на 5 лет"
            ],
            "career": [
                "💼 AI-помощник для карьерного роста",
                "📈 Стратегии позиционирования в эпоху AI",
                "🎤 Переговоры и самопрезентация нового уровня",
                "🌍 Глобальные возможности для специалистов будущего"
            ]
        }
        
        for lesson in course_lessons[course_name]:
            if hash(lesson) == int(lesson_hash):
                update_user_progress(user_id, lesson)
                
                # Возвращаем в меню курса после завершения урока
                text, keyboard = get_course_menu(course_name)
                success_text = f"✅ *Урок отмечен пройденным!*\n\n🎯 Получено: 10 баллов\n📚 Урок: {lesson}\n\n💫 Ваш прогресс растет!\n\n{text}"
                
                edit_main_message(user_id, success_text, keyboard, message_id)
                break

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_callback))

# Вебхук для Flask
@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('UTF-8')
        update = Update.de_json(json_string, application.bot)
        await application.process_update(update)
        return jsonify(success=True)
    return jsonify(success=False)

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    webhook_url = f"{WEBHOOK_URL}"
    result = application.bot.set_webhook(url=WEBHOOK_URL)
    return jsonify(success=result, webhook_url=WEBHOOK_URL)

@app.route('/')
def index():
    return jsonify({
        "status": "AI Education Platform is running!",
        "timestamp": datetime.now().isoformat(),
        "version": "cosmic_ai_1.0"
    })

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

# Запуск Flask
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)