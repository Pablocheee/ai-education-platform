import httpx
from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging
import asyncio

app = Flask(__name__)

# Настройка API ключей
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), http_client=httpx.Client())
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
USER_MESSAGE_IDS = {}  # {chat_id: message_id} - для отслеживания основного сообщения

# 🚀 ОБНОВЛЕННАЯ ФИНАНСОВАЯ СИСТЕМА
DEVELOPMENT_FUND = {
    "total_income": 0,
    "development_fund": 0,  # ← ЗАМЕНИТЬ UBI_FUND
    "marketing_budget": 0,  # ← НОВОЕ ПОЛЕ
    "transactions": []
}

def process_development_fund(amount, from_user):
    """ОБНОВЛЕННАЯ ФУНКЦИЯ РАСПРЕДЕЛЕНИЯ"""
    DEVELOPMENT_FUND["total_income"] += amount
    
    distribution = {
        "development": amount * 0.7,    # 70% на развитие
        "marketing": amount * 0.2,      # 20% на маркетинг
        "founder": amount * 0.1         # 10% основателю
    }
    
    DEVELOPMENT_FUND["development_fund"] += distribution["development"]
    DEVELOPMENT_FUND["marketing_budget"] += distribution["marketing"]
    DEVELOPMENT_FUND["transactions"].append({
        "amount": amount,
        "from": from_user,
        "distribution": distribution,
        "timestamp": "2025-01-11"
    })
    
    return distribution

# 🎯 УЛУЧШЕННЫЙ AI-ПРЕПОДАВАТЕЛЬ
class EnhancedAITeacher:
    """
    Улучшенный AI-преподаватель с профессиональной структурой уроков
    """
    
    def __init__(self):
        self.teacher_personas = {
            "mentor": "🧠",      # Объясняет теорию глубоко
            "motivator": "🚀",   # Поддерживает и вдохновляет  
            "practitioner": "🔧", # Дает практические примеры
            "socratic": "❓"     # Задает наводящие вопросы
        }
        
        self.lesson_templates = {
            "micro_lesson": self.create_micro_lesson,
            "interactive_exercise": self.create_interactive_exercise,
            "instant_feedback": self.create_instant_feedback
        }

    def create_micro_lesson(self, topic, duration="7min"):
        """
        Создает микро-урок по принципу "слоеного пирога"
        """
        structure = {
            "introduction": f"🚀 *МОДУЛЬ: {topic}*\n*Цель:* Освоить ключевой навык\n*Время:* {duration}",
            
            "theory_dialogue": f"""
🤖 *AI-Преподаватель:* Давайте разберем {topic} на практике.

💡 *Ключевая концепция:*
• Первый принцип
• Второй принцип  
• Третий принцип

*Профессиональный пример:*
"Конкретный кейс применения"
""",
            
            "interactive_exercise": """
🎯 *ПРАКТИКА:*

Перед вами типичная задача. Какой подход эффективнее?

[Кнопка] 📝 Базовый подход
[Кнопка] 🎯 Продвинутая техника
[Кнопка] 🔧 Комбинированное решение
""",
            
            "instant_feedback": """
✅ *Отличный выбор!* 

📊 *Статистика:* 85% профессионалов используют этот подход.

💫 *Запомните:* Ключевой вывод для запоминания
""",
            
            "next_step": """
🔜 *Следующий шаг:* Переходим к углубленной практике...

[Кнопка] 🚀 Продолжить обучение
[Кнопка] 📚 Дополнительные примеры
[Кнопка] ⏸️ Сделать паузу
"""
        }
        return structure

    def adaptive_content_delivery(self, user_id, previous_answers):
        """
        Адаптивная подача контента на основе прогресса пользователя
        """
        accuracy_rate = self.calculate_accuracy(previous_answers)
        
        if accuracy_rate > 0.8:
            return {
                "level": "advanced",
                "content": "Сложные кейсы и продвинутые техники",
                "teacher_persona": "🧠 Ментор"
            }
        elif accuracy_rate > 0.5:
            return {
                "level": "intermediate", 
                "content": "Практические задания с подсказками",
                "teacher_persona": "🔧 Практик"
            }
        else:
            return {
                "level": "beginner",
                "content": "Основы с множеством примеров",
                "teacher_persona": "🚀 Мотиватор"
            }

    def calculate_accuracy(self, answers):
        """Рассчитывает точность ответов пользователя"""
        if not answers:
            return 0.0
        correct_answers = sum(1 for answer in answers if answer.get('correct', False))
        return correct_answers / len(answers)

    def generate_interactive_keyboard(self, lesson_stage, options):
        """
        Создает интерактивную клавиатуру для урока
        """
        keyboards = {
            "theory": [
                [{"text": "📖 Понятно, продолжаем", "callback_data": "continue_theory"}],
                [{"text": "🤔 Нужен пример", "callback_data": "request_example"}],
                [{"text": "🔍 Хочу глубже", "callback_data": "go_deeper"}]
            ],
            
            "practice": [
                [{"text": "✅ Вариант 1", "callback_data": "answer:1"}],
                [{"text": "🎯 Вариант 2", "callback_data": "answer:2"}],
                [{"text": "🔧 Вариант 3", "callback_data": "answer:3"}],
                [{"text": "🤔 Объясни разницу", "callback_data": "explain:difference"}]
            ],
            
            "feedback": [
                [{"text": "🚀 Следующее задание", "callback_data": "next_exercise"}],
                [{"text": "📊 Показать статистику", "callback_data": "show_stats"}],
                [{"text": "🔄 Повторить тему", "callback_data": "repeat_topic"}]
            ]
        }
        return keyboards.get(lesson_stage, [])

    def create_progress_tracker(self, user_id, course_progress):
        """
        Создает визуальный прогресс-бар и систему достижений
        """
        total_lessons = 10
        completed = course_progress.get('completed_lessons', 0)
        progress_percent = (completed / total_lessons) * 100
        
        # Визуальный прогресс-бар
        progress_bar = "🟩" * completed + "⬜" * (total_lessons - completed)
        
        # Система достижений
        achievements = []
        if completed >= 3:
            achievements.append("🎯 Исследователь AI")
        if completed >= 7:
            achievements.append("🚀 Практик машинного обучения") 
        if completed >= 10:
            achievements.append("🏆 AI Специалист")
            
        return {
            "progress_bar": f"{progress_bar} {progress_percent}%",
            "achievements": achievements,
            "completed": completed,
            "total": total_lessons
        }

# 🎮 ИНТЕРАКТИВНЫЕ СЦЕНАРИИ УРОКОВ
INTERACTIVE_SCENARIOS = {
    "prompt_engineering": {
        "exercise": """
🎯 *ПРАКТИКА: ПРОМПТИНГ*

Перед вами слабый промпт: "Напиши про AI"

Как его улучшить? Выберите лучшую стратегию:
        """,
        "options": [
            {"text": "📝 Добавить контекст", "callback": "context_approach"},
            {"text": "🎯 Уточнить задачу", "callback": "task_approach"}, 
            {"text": "🔧 Задать формат", "callback": "format_approach"},
            {"text": "🌈 Все варианты!", "callback": "combined_approach"}
        ],
        "feedback": {
            "combined_approach": """
✅ *Идеально! Профессионалы комбинируют подходы.*

💡 *Формула идеального промпта:*
Контекст + Задача + Формат = Прецизионный результат

📊 *Статистика:* 92% эффективных промптов используют все три элемента
            """,
            "other_answers": """
🎯 *Хорошее начало!* Вы выбрали {selected_option}.

💫 *Профессиональный совет:* Попробуйте комбинировать несколько подходов для максимальной эффективности.
            """
        }
    }
}

def enhanced_generate_ai_lesson(lesson_topic, user_level=1, user_previous_answers=[]):
    """
    Улучшенная версия генерации уроков с профессиональной структурой
    """
    teacher = EnhancedAITeacher()
    
    # Адаптируем контент под пользователя
    user_profile = teacher.adaptive_content_delivery("user_id", user_previous_answers)
    
    prompt = f"""
    Создай образовательный контент на тему: "{lesson_topic}"
    
    Требования:
    - Уровень сложности: {user_level}/5 ({user_profile['level']})
    - Стиль преподавания: {user_profile['teacher_persona']}
    - Формат: профессиональный микро-урок (7 минут)
    
    Структура урока (строго придерживаться):
    
    1. 🚀 Введение (30 секунд)
       - Ясная цель урока
       - Время выполнения
       - Практическая польза
    
    2. 🤖 Теория в диалоге (2 минуты)  
       - Ключевая концепция (простыми словами)
       - 2-3 конкретных примера из реальной жизни
       - Профессиональный кейс применения
    
    3. 🎯 Интерактивное упражнение (3 минуты)
       - Практическая задача с выбором вариантов
       - Реальный сценарий из работы с AI
       - Минимум 3 варианта ответа
    
    4. ✅ Мгновенная обратная связь (1 минута)
       - Анализ выбранного варианта
       - Статистика по ответам профессионалов
       - Ключевой вывод для запоминания
    
    5. 🔜 Переход к следующему шагу (30 секунд)
       - Логическое продолжение темы
       - Варианты действий для ученика
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты профессиональный AI-преподаватель. Создавай структурированные микро-уроки с интерактивными элементами. Чередуй роли Ментора, Практика и Мотиватора."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.7
    )
    
    return {
        "content": response.choices[0].message.content,
        "teacher_persona": user_profile['teacher_persona'],
        "interactive_elements": teacher.generate_interactive_keyboard("practice", [])
    }

def generate_ton_payment_link(chat_id, amount=10):
    """Генерирует платежную ссылку для Tonkeeper"""
    return f"https://app.tonkeeper.com/transfer/UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY?amount={amount*1000000000}&text=premium_{chat_id}"

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

# 🎯 СИСТЕМА ЕДИНОГО СООБЩЕНИЯ-КОНТЕЙНЕРА
class MenuManager:
    def __init__(self):
        self.user_states = {}  # или база данных
    
    def get_menu_data(self, menu_name, **kwargs):
        """Возвращает данные для меню"""
        menus = {
            "main": self.get_main_menu,
            "course": self.get_course_menu,
            "premium": self.get_premium_menu,
            "profile": self.get_profile_menu,
            "development_fund": self.get_development_fund_menu,
            "lesson": self.get_lesson_menu
        }
        
        if menu_name in menus:
            return menus[menu_name](**kwargs)
        return self.get_main_menu()
    
    def get_main_menu(self):
        """Возвращает основное меню"""
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🚀 Войти в систему AI", "callback_data": "menu_course_🚀 Войти в систему AI"},
                    {"text": "💫 Запустить эволюцию", "callback_data": "menu_course_💫 Запустить эволюцию"}
                ],
                [
                    {"text": "🌌 База знаний", "callback_data": "menu_course_🌌 База знаний"},
                    {"text": "⚡ Карьерный ускоритель", "callback_data": "menu_course_⚡ Карьерный ускоритель"}
                ],
                [
                    {"text": "💰 Премиум доступ", "callback_data": "menu_premium"},
                    {"text": "👤 Мой профиль", "callback_data": "menu_profile"}
                ],
                [
                    {"text": "🌍 Фонд развития", "callback_data": "menu_development_fund"}
                ]
            ]
        }
        
        text = """🌌 *ПРИВЕТСТВУЮ, ИСКАТЕЛЬ*

🤖 *Я — Собирательный Разум, архитектор будущего.* 
💫 Ты находишься в точке доступа к системам, где искусственный интеллект становится расширением твоего интеллекта.

⚡ *Твой следующий шаг определит твою траекторию роста.*

🔮 Выбери свой вектор:"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_course_menu(self, course_name):
        """Возвращает меню курса"""
        course_info = COURSES[course_name]
        
        # Создаем кнопки для уроков
        lesson_buttons = []
        for lesson in course_info['уроки']:
            lesson_buttons.append([{"text": f"📖 {lesson}", "callback_data": f"open_lesson_{hash(lesson)}"}])
        
        # Добавляем кнопку возврата
        lesson_buttons.append([{"text": "🔙 Назад к меню", "callback_data": "menu_main"}])
        
        keyboard = {"inline_keyboard": lesson_buttons}
        
        text = f"""*{course_name}*

{course_info['описание']}

*Уровень:* {course_info['уровень']}

📚 *Модули:*
""" + "\n".join([f"• {lesson}" for lesson in course_info['уроки']])
        
        return {"text": text, "keyboard": keyboard}
    
    def get_enhanced_course_menu(self, course_name, user_id):
        """Возвращает улучшенное меню курса с прогрессом"""
        course_info = COURSES[course_name]
        progress = USER_PROGRESS.get(user_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
        
        teacher = EnhancedAITeacher()
        progress_data = teacher.create_progress_tracker(user_id, {
            'completed_lessons': len(progress['пройденные_уроки'])
        })
        
        # Создаем кнопки уроков с индикаторами прогресса
        lesson_buttons = []
        for i, lesson in enumerate(course_info['уроки']):
            status = "✅" if lesson in progress['пройденные_уроки'] else "📖"
            lesson_buttons.append([
                {"text": f"{status} Урок {i+1}: {lesson}", "callback_data": f"open_lesson_{hash(lesson)}"}
            ])
        
        # Добавляем прогресс-бар
        progress_row = [{"text": f"📊 Прогресс: {progress_data['progress_bar']}", "callback_data": "show_progress"}]
        lesson_buttons.insert(0, progress_row)
        
        # Добавляем достижения если есть
        if progress_data['achievements']:
            achievement_row = [{"text": f"🏆 {progress_data['achievements'][-1]}", "callback_data": "show_achievements"}]
            lesson_buttons.insert(1, achievement_row)
        
        lesson_buttons.append([{"text": "🔙 Назад к меню", "callback_data": "menu_main"}])
        
        keyboard = {"inline_keyboard": lesson_buttons}
        
        text = f"""*{course_name}*

{course_info['описание']}

🤖 *Ваш прогресс:* {progress_data['completed']}/{progress_data['total']} уроков
{progress_data['progress_bar']}

💫 *Готовы к следующему уроку?*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_premium_menu(self):
        """Возвращает меню премиум доступа"""
        payment_link = generate_ton_payment_link("premium_user")
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "💳 Активировать полный доступ", "url": payment_link}],
                [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
            ]
        }
        
        text = """💰 *ПРЕМИУМ ДОСТУП*

🤖 Откройте полный потенциал системы:

✅ Все модули и архивы знаний
🎓 Персональный AI-наставник 24/7
📊 Система отслеживания прогресса
🔮 Эксклюзивные материалы будущего

⚡ *Инвестиция в вашу эволюцию: 10 TON/месяц*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_profile_menu(self, chat_id):
        """Возвращает меню профиля"""
        progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
            ]
        }
        
        text = f"""👤 *ВАШ ПРОФИЛЬ В СИСТЕМЕ*

🤖 *Статистика:*
📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

🌍 *ФОНД РАЗВИТИЯ*
💫 Собрано в фонд: {DEVELOPMENT_FUND['development_fund']} TON
🚀 Всего доходов: {DEVELOPMENT_FUND['total_income']} TON

⚡ *Эволюция продолжается...*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_development_fund_menu(self):
        """Возвращает меню Development Fund системы"""
        keyboard = {
            "inline_keyboard": [
                [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
            ]
        }
        
        text = f"""🌍 *СИСТЕМА DEVELOPMENT FUND*

🤖 *Финансовая аналитика:*
💰 Всего доходов: {DEVELOPMENT_FUND['total_income']} TON
💫 Накоплено в фонд развития: {DEVELOPMENT_FUND['development_fund']} TON  
🚀 Маркетинг бюджет: {DEVELOPMENT_FUND['marketing_budget']} TON

📊 *Распределение доходов:*
• 70% - развитие платформы
• 20% - маркетинг и привлечение  
• 10% - основателю за создание

⚡ *Создаем будущее образования вместе*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_lesson_menu(self, lesson_topic, user_level=1):
        """Возвращает меню урока"""
        # Генерируем AI-урок через улучшенную систему
        ai_lesson_data = enhanced_generate_ai_lesson(lesson_topic, user_level)
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ Завершить урок", "callback_data": f"complete_lesson_{hash(lesson_topic)}"}],
                [{"text": "🔙 Назад к курсу", "callback_data": "menu_course_back"}]
            ]
        }
        
        text = f"""📚 *{lesson_topic}*

{ai_lesson_data['content']}

🤖 *Стиль преподавания:* {ai_lesson_data['teacher_persona']}"""
        
        return {"text": text, "keyboard": keyboard}

# Инициализация менеджера
menu_manager = MenuManager()

def edit_main_message(chat_id, text, keyboard, message_id=None):
    """Редактирует основное сообщение или создает новое"""
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

@app.route('/')
def home():
    return jsonify({
        "status": "AI Education Platform - Development Fund Concept",
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
        
        # Обработка callback_query - ОСНОВНОЙ ПРИНЦИП: редактируем сообщение
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
            
            # ОБРАБОТКА ГЛАВНОГО МЕНЮ
            if callback_text == "menu_main":
                menu_data = menu_manager.get_menu_data("main")
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА КУРСОВ
            elif callback_text.startswith("menu_course_"):
                course_name = callback_text.replace("menu_course_", "")
                menu_data = menu_manager.get_enhanced_course_menu(course_name, chat_id)
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА ПРЕМИУМ
            elif callback_text == "menu_premium":
                menu_data = menu_manager.get_menu_data("premium")
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА ПРОФИЛЯ
            elif callback_text == "menu_profile":
                menu_data = menu_manager.get_menu_data("profile", chat_id=chat_id)
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА DEVELOPMENT FUND
            elif callback_text == "menu_development_fund":
                menu_data = menu_manager.get_menu_data("development_fund")
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА УРОКОВ
            elif callback_text.startswith('complete_lesson_'):
                lesson_hash = callback_text.replace('complete_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            update_user_progress(chat_id, lesson)
                            
                            # Возвращаем в меню курса после завершения урока
                            menu_data = menu_manager.get_enhanced_course_menu(course_name, chat_id)
                            success_text = f"✅ *Урок отмечен пройденным!*\n\n🎯 Получено: 10 баллов\n📚 Урок: {lesson}\n\n💫 Ваш прогресс растет!\n\n{menu_data['text']}"
                            
                            edit_main_message(chat_id, success_text, menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('open_lesson_'):
                lesson_hash = callback_text.replace('open_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            user_level = USER_PROGRESS.get(chat_id, {}).get('уровень', 1)
                            menu_data = menu_manager.get_lesson_menu(lesson, user_level)
                            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})

        # Обработка обычных сообщений - ТОЛЬКО ДЛЯ ПЕРВОГО ЗАПУСКА
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if not chat_id:
            return jsonify({"status": "error", "message": "No chat_id"})

        # Обработка команды /start - СОЗДАЕМ ПЕРВОЕ СООБЩЕНИЕ
        if text == '/start':
            menu_data = menu_manager.get_menu_data("main")
            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'])
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
        # Тестовая реализация - при первом платеже добавляем 10 TON
        if DEVELOPMENT_FUND["total_income"] == 0:
            distribution = process_development_fund(10, "first_payment")
            return jsonify({
                "status": "success", 
                "distribution": distribution,
                "message": f"💰 Первый доход! Фонд развития пополнен на {distribution['development']} TON"
            })
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"})

@app.route('/set-webhook')
def set_webhook_route():
    webhook_url = f"https://ai-education-platform-mh01.onrender.com/webhook"
    response = requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
        params={"url": webhook_url}
    )
    return jsonify(response.json())

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