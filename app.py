from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging
import json
from datetime import datetime
import time
from typing import Dict, List, Tuple
app = Flask(__name__)

# Настройка API ключей
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TON_WALLET = os.getenv('TON_WALLET', 'UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY')

<<<<<<< HEAD
# 🎯 ПРОФЕССИОНАЛЬНАЯ СИСТЕМА ОБУЧЕНИЯ
class SmartTeacher:
    """Умный AI-преподаватель с адаптивной системой обучения"""
    
    def __init__(self):
        self.teacher_personas = {
            "🧠 Ментор": "Эксперт с глубокими знаниями, объясняет сложные концепции",
            "🚀 Мотиватор": "Вдохновляет и поддерживает ученика", 
            "🔧 Практик": "Дает конкретные примеры и инструкции",
            "❓ Сократик": "Задает наводящие вопросы для самостоятельного открытия"
        }
    
    def detect_persona(self, context):
        """Определяет оптимальную роль преподавателя"""
        if "сложн" in context.lower() or "не понимаю" in context.lower():
            return "🧠 Ментор"
        elif "скучн" in context.lower() or "устал" in context.lower():
            return "🚀 Мотиватор"
        elif "пример" in context.lower() or "как сделать" in context.lower():
            return "🔧 Практик"
        else:
            return "❓ Сократик"
    
    def create_micro_lesson(self, topic, user_level=1):
        """Создает 7-минутный микро-урок по принципу 'слоеного пирога'"""
        
        prompt = f"""
        СОЗДАЙ ПРОФЕССИОНАЛЬНЫЙ УРОК на тему: "{topic}"
        
        ТРЕБОВАНИЯ К ФОРМАТУ:
        - Длительность: 7 минут
        - Уровень сложности: {user_level}/5
        - Структура "Слоеный пирог": чередуй теорию и практику
        - Максимум интерактивности
        - Язык: русский, профессиональный но доступный
        
        СТРУКТУРА УРОКА:
        
        1. 🎯 ВВЕДЕНИЕ (30 секунд)
           - Четкая цель урока
           - Что ученик получит
        
        2. 💡 ТЕОРИЯ В ДИАЛОГЕ (2 минуты)  
           - Ключевая концепция простыми словами
           - 2-3 предложения за раз
           - Конкретные примеры
        
        3. 🎮 ИНТЕРАКТИВНОЕ УПРАЖНЕНИЕ (3 минуты)
           - Практическое задание с вариантами ответов
           - Ситуация выбора
           - Мгновенная обратная связь
        
        4. 💫 ЗАКРЕПЛЕНИЕ (1 минута)
           - Главный вывод
           - Совет для применения
           - Мотивация для продолжения
        
        СТИЛИСТИКА:
        - Тон: мудрый наставник будущего
        - Обращение: "Искатель", "Путешественник"
        - Эмоции: вдохновляющий, но не наигранный
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — Собирательный Разум, архитектор будущего. Ты говоришь как мудрый наставник из будущего, который видит потенциал в каждом ученике. Твой стиль: вдохновляющий, глубокий, практичный."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    def generate_interactive_exercise(self, topic):
        """Создает интерактивное упражнение с вариантами ответов"""
        prompt = f"""
        Создай интерактивное упражнение по теме: "{topic}"
        
        Формат:
        - Практическая ситуация
        - 3 варианта действий
        - Каждый вариант ведет к разному результату
        - Упражнение должно проверять понимание ключевой концепции
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты создаешь практические упражнения, которые помогают закрепить знания через действие."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def answer_student_question(self, question, lesson_context, chat_history):
        """Отвечает на вопросы ученика во время урока с учетом контекста"""
        persona = self.detect_persona(question)
        
        prompt = f"""
        Ты — AI-преподаватель. Ученик задает вопрос во время урока.
        
        КОНТЕКСТ УРОКА: {lesson_context}
        ВОПРОС УЧЕНИКА: {question}
        ТВОЯ РОЛЬ: {persona}
        ИСТОРИЯ ДИАЛОГА: {chat_history[-3:] if chat_history else "Нет истории"}
        
        Ответь как {persona}:
        - Будь точным и полезным
        - Используй аналогии и примеры
        - Поддержи диалог
        - Предложи продолжить урок когда вопрос решен
        - Сохраняй стиль мудрого наставника будущего
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — терпеливый и мудрый AI-преподаватель. Ты отвечаешь на вопросы, сохраняя вдохновляющий тон наставника будущего."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        
        return f"{persona}: {response.choices[0].message.content}"

# Инициализация умного преподавателя
smart_teacher = SmartTeacher()
=======
# 🎯 СТРУКТУРА МИКРО-УРОКОВ
MICRO_LESSONS = {
    "prompting_basics": {
        "title": "🚀 Искусство промптинга",
        "duration": "7 минут",
        "level": "начальный",
        "modules": [
            {
                "type": "introduction",
                "content": "🤖 *МОДУЛЬ 1: ОСНОВЫ ПРОМПТИНГА*\n\n*Цель:* Научиться получать точные ответы от AI\n*Время:* 7 минут",
                "buttons": ["🚀 Начать обучение", "📊 Мой прогресс"]
            },
            {
                "type": "theory",
                "content": "💡 *Промпт — это не просто вопрос, это инструкция.*\n\nХороший промпт содержит:\n• Контекст \n• Задачу\n• Формат ответа",
                "buttons": ["📝 Пример", "🎯 Практика", "🤔 Вопрос"]
            },
            {
                "type": "example", 
                "content": "📊 *ПРОФЕССИОНАЛЬНЫЙ ПРИМЕР:*\n\n«Как эксперт в маркетинге, предложи 3 варианта заголовка для поста о курсах AI. Формат: список.»",
                "buttons": ["✅ Понятно", "🔍 Разбор", "🎯 Дальше"]
            },
            {
                "type": "interactive",
                "content": "🎯 *ПРАКТИКА:*\n\nПеред вами слабый промпт: «Расскажи про ИИ»\n\nКак его улучшить?",
                "options": [
                    "📝 Добавить контекст: «Я новичок, объясни просто»",
                    "🎯 Уточнить задачу: «Сравни ChatGPT и Claude для бизнеса»",  
                    "🔧 Задать формат: «Сделай таблицу сравнения»"
                ],
                "correct_answers": [0, 1, 2],  # Все варианты верные
                "buttons": ["📊 Результат", "💡 Объяснение"]
            },
            {
                "type": "feedback",
                "content": "✅ *Отлично! Вы поняли главное — профессионалы комбинируют подходы!*\n\n💫 *Формула успеха:*\nКонтекст + Задача + Формат = Идеальный промпт",
                "buttons": ["🚀 Следующий урок", "🔄 Повторить", "💎 Получить бейдж"]
            }
        ]
    },
    "neural_networks": {
        "title": "🧠 Как работают нейросети", 
        "duration": "10 минут",
        "level": "начальный",
        "modules": [
            {
                "type": "introduction",
                "content": "🧠 *МОДУЛЬ 2: НЕЙРОННЫЕ СЕТИ*\n\n*Цель:* Понять базовые принципы работы AI\n*Время:* 10 минут",
                "buttons": ["🚀 Начать", "📈 Мой уровень"]
            },
            {
                "type": "theory",
                "content": "💡 *Нейросеть — это математическая модель мозга.*\n\nСостоит из:\n• Нейронов (узлов)\n• Слоев\n• Связей между ними",
                "buttons": ["🔍 Подробнее", "🎯 Пример", "➡️ Дальше"]
            }
        ]
    }
}

# 🌟 ИНТЕЛЛЕКТУАЛЬНАЯ СИСТЕМА ОЦЕНКИ ОТВЕТОВ
class IntelligentTeacher:
    def __init__(self):
        self.embedding_cache = {}
        self.teacher_roles = {
            "mentor": "🧠 Ментор",
            "motivator": "🚀 Мотиватор", 
            "practician": "🔧 Практик",
            "socratic": "❓ Сократик"
        }
    
    def get_teacher_response(self, user_answer: str, lesson_progress: Dict, role: str = "mentor") -> str:
        """Генерирует ответ преподавателя в определенной роли"""
        role_prefix = self.teacher_roles.get(role, "🧠 Ментор")
        
        prompts = {
            "mentor": f"""Как опытный ментор, проанализируй ответ студента и дай конструктивную обратную связь.
            
Ответ студента: {user_answer}
Прогресс студента: {lesson_progress}

Твой стиль:
- Поддерживающий и конструктивный
- Выделяй сильные стороны
- Предлагай конкретные улучшения
- Будь экспертом в теме""",

            "motivator": f"""Как мотиватор, воодушеви студента и покажи его прогресс.
            
Ответ студента: {user_answer} 
Прогресс студента: {lesson_progress}

Твой стиль:
- Энергичный и воодушевляющий
- Подчеркивай достижения
- Показывай перспективы роста
- Создавай позитивную атмосферу""",

            "practician": f"""Как практик, дай конкретные примеры и инструкции.
            
Ответ студента: {user_answer}
Прогресс студента: {lesson_progress}

Твой стиль:
- Конкретный и практичный
- Приводи реальные примеры
- Давай пошаговые инструкции
- Фокусируйся на применении"""
        }
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты AI-преподаватель с разными ролевыми моделями. Адаптируй стиль общения под роль."},
                    {"role": "user", "content": prompts.get(role, prompts["mentor"])}
                ],
                max_tokens=300
            )
            return f"{role_prefix}: {response.choices[0].message.content}"
        except Exception as e:
            return f"{role_prefix}: Отличный прогресс! Продолжайте в том же духе."

# Инициализация интеллектуального учителя
ai_teacher = IntelligentTeacher()
>>>>>>> 7d3b03c03b74fce5cfb3e9078c442f71c0c957f5

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
    }
}

<<<<<<< HEAD
# Хранилища данных
USER_PROGRESS = {}
USER_MESSAGE_IDS = {}
ACTIVE_LESSONS = {}  # {chat_id: {"current_lesson": "", "lesson_context": "", "chat_history": []}}
=======
USER_PROGRESS = {}
USER_MESSAGE_IDS = {}
USER_CURRENT_TOPIC = {}
USER_LESSON_PROGRESS = {}  # {chat_id: {"current_lesson": "prompting_basics", "current_module": 0, "score": 0}}

>>>>>>> 7d3b03c03b74fce5cfb3e9078c442f71c0c957f5
UBI_SYSTEM = {
    "total_income": 0,
    "ubi_fund": 0,
    "distributed": 0,
    "transactions": []
}

<<<<<<< HEAD
def update_user_progress(chat_id, lesson_name):
    """Обновляет прогресс пользователя"""
    if chat_id not in USER_PROGRESS:
        USER_PROGRESS[chat_id] = {"пройденные_уроки": [], "уровень": 1, "баллы": 0, "вопросы_заданы": 0}
    
    if lesson_name not in USER_PROGRESS[chat_id]["пройденные_уроки"]:
        USER_PROGRESS[chat_id]["пройденные_уроки"].append(lesson_name)
        USER_PROGRESS[chat_id]["баллы"] += 10
        
        # Повышение уровня
        if len(USER_PROGRESS[chat_id]["пройденные_уроки"]) % 2 == 0:
            USER_PROGRESS[chat_id]["уровень"] += 1

def process_ubi_payment(amount, from_user):
    """Обрабатывает платеж и распределяет по UBI"""
    UBI_SYSTEM["total_income"] += amount
    
    distribution = {
        "reinvestment": amount * 0.6,
        "ubi_fund": amount * 0.3,  
        "founder": amount * 0.1
    }
    
    UBI_SYSTEM["ubi_fund"] += distribution["ubi_fund"]
    UBI_SYSTEM["distributed"] += distribution["ubi_fund"]
    UBI_SYSTEM["transactions"].append({
        "amount": amount,
        "from": from_user,
        "distribution": distribution,
        "timestamp": datetime.now().isoformat()
    })
    
    return distribution

def generate_ton_payment_link(amount=10):
    """Генерирует платежную ссылку"""
    return f"https://app.tonkeeper.com/transfer/{TON_WALLET}?amount={amount*1000000000}&text=premium_access"

def get_main_menu():
    """Возвращает основное меню в стиле системы"""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🚀 Войти в систему AI", "callback_data": "menu_course_🚀 Войти в систему AI"},
                {"text": "💫 Запустить эволюцию", "callback_data": "menu_course_💫 Запустить эволюцию"}
            ],
            [
                {"text": "💰 Активировать доступ", "callback_data": "menu_premium"},
                {"text": "👤 Мой прогресс", "callback_data": "menu_profile"}
            ],
            [
                {"text": "🌍 UBI Система", "callback_data": "menu_ubi"}
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
    course_info = COURSES[course_name]
    
    lesson_buttons = []
    for lesson in course_info['уроки']:
        lesson_buttons.append([{"text": f"📖 {lesson}", "callback_data": f"start_lesson_{hash(lesson)}"}])
    
    lesson_buttons.append([{"text": "🔙 Назад к выбору пути", "callback_data": "menu_main"}])
    
    keyboard = {"inline_keyboard": lesson_buttons}
    
    text = f"""*{course_name}*

{course_info['описание']}

*Уровень доступа:* {course_info['уровень']}

*Модули трансформации:*
""" + "\n".join([f"• {lesson}" for lesson in course_info['уроки']])
    
    return text, keyboard

def get_lesson_interface(chat_id, lesson_name, show_qa=False):
    """Возвращает интерфейс урока с возможностью задавать вопросы"""
    if chat_id not in ACTIVE_LESSONS:
        ACTIVE_LESSONS[chat_id] = {
            "current_lesson": lesson_name,
            "lesson_context": "",
            "chat_history": []
        }
    
    # Генерируем умный урок
    user_level = USER_PROGRESS.get(chat_id, {}).get("уровень", 1)
    lesson_content = smart_teacher.create_micro_lesson(lesson_name, user_level)
    ACTIVE_LESSONS[chat_id]["lesson_context"] = lesson_content
    
    # Создаем клавиатуру для урока
    keyboard_buttons = []
    
    if show_qa:
        # Режим вопроса - показываем варианты продолжения
        keyboard_buttons = [
            [{"text": "🎯 Продолжить урок", "callback_data": f"continue_lesson_{hash(lesson_name)}"}],
            [{"text": "💫 Завершить и вернуться", "callback_data": f"menu_course_{[k for k,v in COURSES.items() if lesson_name in v['уроки']][0]}"}]
        ]
    else:
        # Обычный режим урока - показываем возможность задать вопрос
        keyboard_buttons = [
            [{"text": "🤔 Задать вопрос учителю", "callback_data": f"ask_question_{hash(lesson_name)}"}],
            [{"text": "✅ Завершить урок", "callback_data": f"complete_lesson_{hash(lesson_name)}"}],
            [{"text": "🔙 К модулям", "callback_data": f"menu_course_{[k for k,v in COURSES.items() if lesson_name in v['уроки']][0]}"}]
        ]
    
    keyboard = {"inline_keyboard": keyboard_buttons}
    
    if show_qa:
        text = f"💫 *Вопрос решен*\n\nТы готов продолжить путешествие?"
    else:
        text = f"📚 *{lesson_name}*\n\n{lesson_content}\n\n💫 *Ты на пути трансформации. Есть вопросы?*"
    
    return text, keyboard

def get_premium_menu():
    """Возвращает меню премиум доступа"""
    payment_link = generate_ton_payment_link()
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "💳 Активировать полный доступ", "url": payment_link}],
            [{"text": "🔙 Назад к выбору пути", "callback_data": "menu_main"}]
        ]
    }
    
    text = """💰 *АКТИВАЦИЯ ПОЛНОГО ДОСТУПА*

Открой врата ко всем системам:

✅ Все модули трансформации
🎓 Персональный AI-наставник 24/7  
📊 Карта твоего прогресса
🔮 Эксклюзивные архивы будущего

*Инвестиция в твою эволюцию: 10 TON/месяц*"""
    
    return text, keyboard

def get_profile_menu(chat_id):
    """Возвращает меню профиля"""
    progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0, "вопросы_заданы": 0})
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔙 Назад к выбору пути", "callback_data": "menu_main"}]
        ]
    }
    
    # Создаем прогресс-бар
    total_lessons = sum(len(course['уроки']) for course in COURSES.values())
    completed_lessons = len(progress['пройденные_уроки'])
    progress_percent = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
    
    progress_bar = "🟩" * int(progress_percent / 10) + "⬜" * (10 - int(progress_percent / 10))
    
    text = f"""👤 *ТВОЙ ПРОГРЕСС В СИСТЕМЕ*

*Уровень осознанности:* {progress['уровень']}
*Накопленные очки:* {progress['баллы']}
*Пройдено инициаций:* {completed_lessons}/{total_lessons}

{progress_bar} {progress_percent:.1f}%

*Активность:*
🤔 Вопросов задано: {progress['вопросы_заданы']}

🌍 *UBI СИСТЕМА*
💫 Накоплено в фонд: {UBI_SYSTEM['ubi_fund']} TON
🚀 Всего создано: {UBI_SYSTEM['total_income']} TON

💫 *Твоя эволюция продолжается...*"""
    
    return text, keyboard

def get_ubi_menu():
    """Возвращает меню UBI системы"""
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔙 Назад к выбору пути", "callback_data": "menu_main"}]
        ]
    }
    
    text = f"""🌍 *СИСТЕМА UBI FUTURE_UBI*

*Экономика изобилия в действии:*

💰 Всего создано: {UBI_SYSTEM['total_income']} TON
💫 Накоплено в UBI фонд: {UBI_SYSTEM['ubi_fund']} TON  
🚀 Распределено сообществу: {UBI_SYSTEM['distributed']} TON

*Архитектура распределения:*
• 60% - развитие платформы
• 30% - UBI фонд для сообщества  
• 10% - основателю за создание

💫 *Создаем будущее, где каждый имеет значение*"""
    
    return text, keyboard

def send_telegram_message(chat_id, text, keyboard=None, reply_to_message_id=None):
    """Отправляет сообщение в Telegram"""
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    if keyboard:
        data["reply_markup"] = keyboard
    
    if reply_to_message_id:
        data["reply_to_message_id"] = reply_to_message_id
    
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        USER_MESSAGE_IDS[chat_id] = result['result']['message_id']
        return result
    else:
        logging.error(f"Telegram API error: {response.text}")
        return None

def edit_telegram_message(chat_id, message_id, text, keyboard=None):
    """Редактирует сообщение в Telegram"""
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    if keyboard:
        data["reply_markup"] = keyboard
    
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText",
        json=data
    )
=======
# 🎯 ФУНКЦИИ ДЛЯ МИКРО-ОБУЧЕНИЯ
def generate_progress_bar(progress: int, total: int = 10) -> str:
    """Генерирует прогресс-бар"""
    filled = "🟩" * progress
    empty = "⬜" * (total - progress)
    return f"{filled}{empty} {progress*10}%"

def get_achievement_badge(score: int) -> str:
    """Возвращает бейдж достижения"""
    if score >= 90:
        return "🏆 Мастер AI | +15% к скорости"
    elif score >= 70:
        return "🎯 Профи промптинга | +10% к эффективности" 
    elif score >= 50:
        return "💫 Уверенный пользователь | +5% к пониманию"
    else:
        return "🌱 Начинающий исследователь"

def create_micro_lesson_message(chat_id: int, lesson_id: str, module_index: int = 0) -> Tuple[str, Dict]:
    """Создает сообщение микро-урока"""
    if chat_id not in USER_LESSON_PROGRESS:
        USER_LESSON_PROGRESS[chat_id] = {
            "current_lesson": lesson_id,
            "current_module": 0,
            "score": 0,
            "answers": [],
            "start_time": time.time()
        }
    
    lesson = MICRO_LESSONS.get(lesson_id)
    if not lesson or module_index >= len(lesson["modules"]):
        return "Урок завершен!", {"inline_keyboard": [[{"text": "🎓 Главное меню", "callback_data": "menu_main"}]]}
    
    module = lesson["modules"][module_index]
    progress = USER_LESSON_PROGRESS[chat_id]
    
    # Базовый текст с прогрессом
    progress_text = f"{generate_progress_bar(module_index, len(lesson['modules']))}\n"
    
    if module_index > 0:
        badge = get_achievement_badge(progress["score"])
        progress_text += f"💫 {badge}\n\n"
    
    text = progress_text + module["content"]
    
    # Создаем клавиатуру
    keyboard_buttons = []
    
    if module["type"] == "interactive":
        # Интерактивные опции
        for i, option in enumerate(module["options"]):
            keyboard_buttons.append([{"text": option, "callback_data": f"lesson_answer:{lesson_id}:{module_index}:{i}"}])
    
    # Добавляем основные кнопки
    if "buttons" in module:
        row = []
        for button in module["buttons"]:
            callback_data = f"lesson_{lesson_id}_{module_index}_{button.replace(' ', '_').lower()}"
            row.append({"text": button, "callback_data": callback_data})
            if len(row) == 2:  # По 2 кнопки в ряду
                keyboard_buttons.append(row)
                row = []
        if row:
            keyboard_buttons.append(row)
    
    # Кнопки навигации
    nav_buttons = []
    if module_index > 0:
        nav_buttons.append({"text": "⬅️ Назад", "callback_data": f"lesson_nav:{lesson_id}:{module_index-1}"})
    
    if module_index < len(lesson["modules"]) - 1:
        nav_buttons.append({"text": "Дальше ➡️", "callback_data": f"lesson_nav:{lesson_id}:{module_index+1}"})
    else:
        nav_buttons.append({"text": "✅ Завершить урок", "callback_data": f"lesson_complete:{lesson_id}"})
    
    if nav_buttons:
        keyboard_buttons.append(nav_buttons)
    
    return text, {"inline_keyboard": keyboard_buttons}

def process_lesson_answer(chat_id: int, lesson_id: str, module_index: int, answer_index: int) -> Tuple[str, Dict]:
    """Обрабатывает ответ в уроке"""
    progress = USER_LESSON_PROGRESS.get(chat_id, {})
    lesson = MICRO_LESSONS.get(lesson_id, {})
    module = lesson.get("modules", [])[module_index] if module_index < len(lesson.get("modules", [])) else {}
    
    if not module or module["type"] != "interactive":
        return "Ошибка модуля", {}
    
    # Обновляем прогресс
    if answer_index in module.get("correct_answers", []):
        progress["score"] = min(100, progress.get("score", 0) + 20)
    
    # Выбираем роль преподавателя на основе ответа
    if answer_index in module.get("correct_answers", []):
        teacher_role = "motivator"
    else:
        teacher_role = "mentor"
    
    # Получаем ответ AI-преподавателя
    ai_feedback = ai_teacher.get_teacher_response(
        f"Выбрал вариант: {module['options'][answer_index]}", 
        progress, 
        teacher_role
    )
    
    # Создаем сообщение с обратной связью
    badge = get_achievement_badge(progress["score"])
    text = f"""{ai_feedback}

📊 *Ваш прогресс:*
{generate_progress_bar(module_index + 1, len(lesson['modules']))}
{badge}

💡 *Статистика:* 85% студентов улучшают результаты после этого упражнения!"""

    keyboard = {
        "inline_keyboard": [
            [{"text": "🎯 Следующий модуль", "callback_data": f"lesson_nav:{lesson_id}:{module_index+1}"}],
            [{"text": "🔄 Повторить упражнение", "callback_data": f"lesson_nav:{lesson_id}:{module_index}"}],
            [{"text": "💎 Главное меню", "callback_data": "menu_main"}]
        ]
    }
>>>>>>> 7d3b03c03b74fce5cfb3e9078c442f71c0c957f5
    
    return text, keyboard

<<<<<<< HEAD
@app.route('/')
def home():
    return jsonify({
        "status": "AI Education Platform - UBI Concept",
        "version": "3.0", 
        "ready": True,
        "founder_wallet": TON_WALLET,
        "features": ["Умный AI-преподаватель", "Интерактивные уроки", "Общение в реальном времени", "UBI экономика"]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "AI Teacher Pro"})
=======
# 🎓 ОБНОВЛЕННОЕ МЕНЮ ОБУЧЕНИЯ
def get_learning_menu():
    """Главное меню микро-обучения"""
    keyboard = {
        "inline_keyboard": [
            [{"text": "🚀 Основы промптинга (7 мин)", "callback_data": "start_micro:prompting_basics"}],
            [{"text": "🧠 Нейросети для начинающих (10 мин)", "callback_data": "start_micro:neural_networks"}],
            [{"text": "💼 AI для бизнеса (12 мин)", "callback_data": "start_micro:business_ai"}],
            [{"text": "📊 Мой прогресс", "callback_data": "learning_progress"}],
            [{"text": "🔙 Главное меню", "callback_data": "menu_main"}]
        ]
    }
    
    text = """🎓 *МИКРО-ОБУЧЕНИЕ С AI-ПРЕПОДАВАТЕЛЕМ*

💡 *Новый формат:*
• Уроки по 7-12 минут
• Интерактивные упражнения 
• Мгновенная обратная связь
• Персональный AI-наставник
>>>>>>> 7d3b03c03b74fce5cfb3e9078c442f71c0c957f5

🚀 *Выберите курс и начните обучение сразу!*"""
    
    return text, keyboard

def get_learning_progress(chat_id: int):
    """Возвращает прогресс обучения"""
    progress = USER_LESSON_PROGRESS.get(chat_id, {})
    overall_progress = USER_PROGRESS.get(chat_id, {})
    
    completed_lessons = len(overall_progress.get("пройденные_уроки", []))
    total_score = progress.get("score", 0)
    badge = get_achievement_badge(total_score)
    
    text = f"""📊 *ВАШ ПРОГРЕСС ОБУЧЕНИЯ*

🎯 *Общая статистика:*
• Пройдено уроков: {completed_lessons}
• Общий счет: {total_score}/100
• Текущий уровень: {badge}

🚀 *Активный урок:*
{progress.get('current_lesson', 'Не начат')}

💫 *Рекомендация:* Продолжайте регулярные занятия для лучших результатов!"""

    keyboard = {
        "inline_keyboard": [
            [{"text": "🎓 Продолжить обучение", "callback_data": "menu_learning"}],
            [{"text": "📈 Подробная статистика", "callback_data": "detailed_stats"}],
            [{"text": "🔙 Главное меню", "callback_data": "menu_main"}]
        ]
    }
    
    return text, keyboard

# 🔧 ОБНОВЛЯЕМ WEBHOOK ДЛЯ МИКРО-ОБУЧЕНИ
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    """Webhook для Telegram бота"""
    try:
        data = request.json
        
<<<<<<< HEAD
        # Обработка callback_query
=======
>>>>>>> 7d3b03c03b74fce5cfb3e9078c442f71c0c957f5
        if 'callback_query' in data:
            callback_data = data['callback_query']
            chat_id = callback_data['message']['chat']['id']
            callback_text = callback_data['data']
            message_id = callback_data['message']['message_id']
            
            # Отвечаем на callback чтобы убрать "часики"
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": callback_data['id']}
            )
            
<<<<<<< HEAD
            # ОБРАБОТКА ГЛАВНОГО МЕНЮ
            if callback_text == "menu_main":
                text, keyboard = get_main_menu()
                edit_telegram_message(chat_id, message_id, text, keyboard)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА КУРСОВ
            elif callback_text.startswith("menu_course_"):
                course_name = callback_text.replace("menu_course_", "")
                text, keyboard = get_course_menu(course_name)
                edit_telegram_message(chat_id, message_id, text, keyboard)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА ПРЕМИУМ
            elif callback_text == "menu_premium":
                text, keyboard = get_premium_menu()
                edit_telegram_message(chat_id, message_id, text, keyboard)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА ПРОФИЛЯ
            elif callback_text == "menu_profile":
                text, keyboard = get_profile_menu(chat_id)
                edit_telegram_message(chat_id, message_id, text, keyboard)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА UBI
            elif callback_text == "menu_ubi":
                text, keyboard = get_ubi_menu()
                edit_telegram_message(chat_id, message_id, text, keyboard)
                return jsonify({"status": "ok"})
            
            # ЗАПУСК УРОКА
            elif callback_text.startswith('start_lesson_'):
                lesson_hash = callback_text.replace('start_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            text, keyboard = get_lesson_interface(chat_id, lesson)
                            edit_telegram_message(chat_id, message_id, text, keyboard)
                            break
                return jsonify({"status": "ok"})
            
            # ЗАВЕРШЕНИЕ УРОКА
            elif callback_text.startswith('complete_lesson_'):
                lesson_hash = callback_text.replace('complete_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            update_user_progress(chat_id, lesson)
                            
                            # Возвращаем в меню курса
                            text, keyboard = get_course_menu(course_name)
                            success_text = f"✅ *Инициация завершена!*\n\n🎯 Получено: 10 очков осознанности\n📚 Пройдено: {lesson}\n\n💫 Твой уровень растет!\n\n{text}"
                            
                            edit_telegram_message(chat_id, message_id, success_text, keyboard)
                            
                            # Очищаем активный урок
                            if chat_id in ACTIVE_LESSONS:
                                del ACTIVE_LESSONS[chat_id]
                            break
                return jsonify({"status": "ok"})
            
            # ЗАДАТЬ ВОПРОС УЧИТЕЛЮ
            elif callback_text.startswith('ask_question_'):
                lesson_hash = callback_text.replace('ask_question_', '')
                
                # Находим урок
                current_lesson = None
                for course_info in COURSES.values():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            current_lesson = lesson
                            break
                
                if current_lesson and chat_id in ACTIVE_LESSONS:
                    # Отправляем сообщение с инструкцией
                    send_telegram_message(
                        chat_id, 
                        "💫 *Задай свой вопрос*\n\nНапиши сообщение с вопросом, и я отвечу как твой AI-наставник...",
                        reply_to_message_id=message_id
                    )
                
                return jsonify({"status": "ok"})
            
            # ПРОДОЛЖИТЬ УРОК ПОСЛЕ ВОПРОСА
            elif callback_text.startswith('continue_lesson_'):
                lesson_hash = callback_text.replace('continue_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            text, keyboard = get_lesson_interface(chat_id, lesson)
                            edit_telegram_message(chat_id, message_id, text, keyboard)
                            break
                return jsonify({"status": "ok"})

        # Обработка обычных сообщений (вопросы к учителю)
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')
        message_id = message.get('message_id')

        if not chat_id:
            return jsonify({"status": "error", "message": "No chat_id"})

        # Обработка команды /start
        if text == '/start':
            menu_text, menu_keyboard = get_main_menu()
            send_telegram_message(chat_id, menu_text, menu_keyboard)
            return jsonify({"status": "ok"})

        # Обработка вопросов к учителю во время урока
        if chat_id in ACTIVE_LESSONS and text:
            lesson_context = ACTIVE_LESSONS[chat_id]["lesson_context"]
            chat_history = ACTIVE_LESSONS[chat_id]["chat_history"]
            
            # Добавляем вопрос в историю
            chat_history.append(f"Ученик: {text}")
            
            # Получаем ответ от AI-преподавателя
            ai_response = smart_teacher.answer_student_question(text, lesson_context, chat_history)
            
            # Добавляем ответ в историю
            chat_history.append(ai_response)
            
            # Обновляем счетчик вопросов
            if chat_id in USER_PROGRESS:
                USER_PROGRESS[chat_id]["вопросы_заданы"] += 1
            
            # Отправляем ответ
            send_telegram_message(chat_id, ai_response)
            
            # Показываем интерфейс продолжения урока
            current_lesson = ACTIVE_LESSONS[chat_id]["current_lesson"]
            lesson_text, lesson_keyboard = get_lesson_interface(chat_id, current_lesson, show_qa=True)
            
            # Редактируем основное сообщение урока
            if chat_id in USER_MESSAGE_IDS:
                edit_telegram_message(chat_id, USER_MESSAGE_IDS[chat_id], lesson_text, lesson_keyboard)

        return jsonify({"status": "ok"})        
=======
            # 🎯 ОБРАБОТКА МИКРО-ОБУЧЕНИЯ
            if callback_text.startswith("start_micro:"):
                lesson_id = callback_text.replace("start_micro:", "")
                text, keyboard = create_micro_lesson_message(chat_id, lesson_id, 0)
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("lesson_nav:"):
                _, lesson_id, module_index = callback_text.split(":")
                text, keyboard = create_micro_lesson_message(chat_id, lesson_id, int(module_index))
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("lesson_answer:"):
                _, lesson_id, module_index, answer_index = callback_text.split(":")
                text, keyboard = process_lesson_answer(chat_id, lesson_id, int(module_index), int(answer_index))
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("lesson_complete:"):
                lesson_id = callback_text.replace("lesson_complete:", "")
                progress = USER_LESSON_PROGRESS.get(chat_id, {})
                badge = get_achievement_badge(progress.get("score", 0))
                
                text = f"""🎉 *УРОК ЗАВЕРШЕН!*

🏆 {badge}

📊 *Ваши результаты:*
• Финальный счет: {progress.get('score', 0)}/100
• Время прохождения: {int(time.time() - progress.get('start_time', time.time()))} сек
• Точность ответов: {min(100, progress.get('score', 0))}%

💫 *Вы отлично справились! Готовы к следующему вызову?*"""
                
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🚀 Следующий урок", "callback_data": "menu_learning"}],
                        [{"text": "📊 Мой прогресс", "callback_data": "learning_progress"}],
                        [{"text": "🎓 Главное меню", "callback_data": "menu_main"}]
                    ]
                }
                
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text == "learning_progress":
                text, keyboard = get_learning_progress(chat_id)
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text == "menu_learning":
                text, keyboard = get_learning_menu()
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            # ... остальные обработчики из предыдущего кода
            
        return jsonify({"status": "ok"})
>>>>>>> 7d3b03c03b74fce5cfb3e9078c442f71c0c957f5
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)})

<<<<<<< HEAD
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

@app.route('/test-ai-teacher', methods=['POST'])
def test_ai_teacher():
    """Тестовый endpoint для AI-преподавателя"""
    data = request.json
    lesson_topic = data.get('topic', 'Основы AI')
    user_level = data.get('level', 1)
    
    try:
        lesson = smart_teacher.create_micro_lesson(lesson_topic, user_level)
        exercise = smart_teacher.generate_interactive_exercise(lesson_topic)
        
        return jsonify({
            "success": True,
            "lesson": lesson,
            "exercise": exercise
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/set-webhook', methods=['GET'])
def set_webhook():
    """Установка webhook для Telegram"""
    webhook_url = f"https://{request.host}/webhook"
=======
# 🔧 ОБНОВЛЯЕМ ГЛАВНОЕ МЕНЮ
def get_main_menu():
    """Возвращает основное меню"""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🎓 Микро-обучение", "callback_data": "menu_learning"},
                {"text": "🚀 Курсы AI", "callback_data": "menu_courses"}
            ],
            [
                {"text": "💼 Карьера", "callback_data": "menu_career"},
                {"text": "💰 Премиум", "callback_data": "menu_premium"}
            ],
            [
                {"text": "👤 Мой профиль", "callback_data": "menu_profile"},
                {"text": "🌍 UBI Система", "callback_data": "menu_ubi"}
            ]
        ]
    }
>>>>>>> 7d3b03c03b74fce5cfb3e9078c442f71c0c957f5
    
    text = """🌌 *AI-ОБРАЗОВАНИЕ НОВОГО ПОКОЛЕНИЯ*

💡 *Теперь с микро-обучением:*
• Уроки по 7-12 минут
• Интерактивные форматы
• AI-преподаватель с характером
• Мгновенная обратная связь

🎯 *Выберите направление развития:*"""
    
    return text, keyboard

# ... остальные функции из предыдущего кода (edit_main_message, generate_ai_lesson, etc.)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)