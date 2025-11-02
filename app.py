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
USER_LESSON_STATE = {}  # {chat_id: {"current_lesson": "", "step": 0, "answers": []}}

# 🚀 ОБНОВЛЕННАЯ ФИНАНСОВАЯ СИСТЕМА
DEVELOPMENT_FUND = {
    "total_income": 0,
    "development_fund": 0,
    "marketing_budget": 0,
    "transactions": []
}

def process_development_fund(amount, from_user):
    """ОБНОВЛЕННАЯ ФУНКЦИЯ РАСПРЕДЕЛЕНИЯ"""
    DEVELOPMENT_FUND["total_income"] += amount
    
    distribution = {
        "development": amount * 0.7,
        "marketing": amount * 0.2,
        "founder": amount * 0.1
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

# 🎯 УЛУЧШЕННЫЙ AI-ПРЕПОДАВАТЕЛЬ С ИНТЕРАКТИВОМ
class InteractiveAITeacher:
    def __init__(self):
        self.teacher_styles = {
            "mentor": "🧠",
            "motivator": "🚀",  
            "practitioner": "🔧",
            "socratic": "❓"
        }

    def generate_interactive_lesson(self, topic, user_level=1):
        """Генерирует интерактивный урок с вопросами"""
        prompt = f"""
        Создай интерактивный урок на тему: "{topic}"
        
        Структура (строго):
        1. КРАТКОЕ введение (2-3 предложения)
        2. 1 ключевой вопрос для ученика с 3 вариантами ответа
        3. Объяснение правильного ответа
        
        Уровень сложности: {user_level}/5
        Формат: диалоговый, вовлекающий
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты AI-преподаватель. Создавай короткие интерактивные уроки с вопросами и вариантами ответов."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return self._parse_lesson_response(response.choices[0].message.content)

    def _parse_lesson_response(self, text):
        """Парсит ответ AI на структурированные компоненты"""
        lines = text.split('\n')
        lesson_data = {
            "introduction": "",
            "question": "",
            "options": [],
            "explanation": ""
        }
        
        current_section = "introduction"
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "?" in line and not lesson_data["question"]:
                lesson_data["question"] = line
                current_section = "options"
            elif current_section == "options" and any(marker in line for marker in ["1)", "2)", "3)", "•", "-"]):
                clean_option = line.split(')', 1)[-1].split('.', 1)[-1].strip()
                if clean_option and len(lesson_data["options"]) < 3:
                    lesson_data["options"].append(clean_option)
            elif current_section == "options" and line and not any(marker in line for marker in ["1)", "2)", "3)"]):
                current_section = "explanation"
                lesson_data["explanation"] = line
            elif current_section == "explanation":
                lesson_data["explanation"] += " " + line
            elif not lesson_data["introduction"]:
                lesson_data["introduction"] = line
        
        # Заполняем недостающие опции
        while len(lesson_data["options"]) < 3:
            lesson_data["options"].append(f"Вариант {len(lesson_data['options']) + 1}")
            
        return lesson_data

    def create_progress_tracker(self, completed_lessons, total_lessons=10):
        """Создает визуальный прогресс-бар"""
        progress_percent = (completed_lessons / total_lessons) * 100
        progress_bar = "🟩" * completed_lessons + "⬜" * (total_lessons - completed_lessons)
        
        achievements = []
        if completed_lessons >= 3:
            achievements.append("🎯 Исследователь AI")
        if completed_lessons >= 7:
            achievements.append("🚀 Практик AI") 
        if completed_lessons >= 10:
            achievements.append("🏆 AI Специалист")
            
        return {
            "progress_bar": f"{progress_bar} {progress_percent:.1f}%",
            "achievements": achievements,
            "completed": completed_lessons,
            "total": total_lessons
        }

# Инициализация преподавателя
interactive_teacher = InteractiveAITeacher()

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
        
        if len(USER_PROGRESS[chat_id]["пройденные_уроки"]) % 4 == 0:
            USER_PROGRESS[chat_id]["уровень"] += 1

def update_lesson_state(chat_id, lesson_name, step=0, answers=None):
    """Обновляет состояние урока пользователя"""
    if chat_id not in USER_LESSON_STATE:
        USER_LESSON_STATE[chat_id] = {}
    
    USER_LESSON_STATE[chat_id] = {
        "current_lesson": lesson_name,
        "step": step,
        "answers": answers or []
    }

# 🎯 СИСТЕМА МЕНЮ
class MenuManager:
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
    
    def get_enhanced_course_menu(self, course_name, user_id):
        """Возвращает улучшенное меню курса с прогрессом"""
        course_info = COURSES[course_name]
        progress = USER_PROGRESS.get(user_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
        
        progress_data = interactive_teacher.create_progress_tracker(
            len(progress['пройденные_уроки'])
        )
        
        lesson_buttons = []
        for i, lesson in enumerate(course_info['уроки']):
            status = "✅" if lesson in progress['пройденные_уроки'] else "📖"
            lesson_buttons.append([
                {"text": f"{status} Урок {i+1}: {lesson}", "callback_data": f"open_lesson_{hash(lesson)}"}
            ])
        
        progress_row = [{"text": f"📊 Прогресс: {progress_data['progress_bar']}", "callback_data": "show_progress"}]
        lesson_buttons.insert(0, progress_row)
        
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
    
    def get_interactive_lesson(self, lesson_topic, user_level=1):
        """Возвращает интерактивный урок"""
        lesson_data = interactive_teacher.generate_interactive_lesson(lesson_topic, user_level)
        
        # Создаем кнопки для вариантов ответа
        options_buttons = []
        for i, option in enumerate(lesson_data["options"]):
            options_buttons.append([{"text": f"{i+1}. {option}", "callback_data": f"answer_{i}_{hash(lesson_topic)}"}])
        
        options_buttons.append([{"text": "🔙 Назад к курсу", "callback_data": "menu_course_back"}])
        
        keyboard = {"inline_keyboard": options_buttons}
        
        text = f"""📚 *{lesson_topic}*

{lesson_data['introduction']}

🎯 *Вопрос:*
{lesson_data['question']}

💡 *Выберите вариант ответа:*"""
        
        return {"text": text, "keyboard": keyboard, "lesson_data": lesson_data}
    
    def get_lesson_feedback(self, user_answer, correct_answer, explanation, lesson_topic):
        """Возвращает обратную связь по ответу"""
        is_correct = user_answer == correct_answer
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ Завершить урок", "callback_data": f"complete_lesson_{hash(lesson_topic)}"}],
                [{"text": "🔄 Повторить тему", "callback_data": f"open_lesson_{hash(lesson_topic)}"}],
                [{"text": "🔙 Назад к курсу", "callback_data": "menu_course_back"}]
            ]
        }
        
        if is_correct:
            text = f"""🎉 *Правильно!*

{explanation}

💫 *Отличная работа! Вы усвоили материал.*"""
        else:
            text = f"""🤔 *Почти правильно!*

{explanation}

💡 *Попробуйте ещё раз - это поможет лучше запомнить материал.*"""
        
        return {"text": text, "keyboard": keyboard}

# Инициализация менеджера
menu_manager = MenuManager()

def edit_main_message(chat_id, text, keyboard, message_id=None):
    """Редактирует основное сообщение или создает новое"""
    if message_id and chat_id in USER_MESSAGE_IDS:
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
        "status": "AI Education Platform - Interactive Version",
        "version": "3.1", 
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
        
        if 'callback_query' in data:
            callback_data = data['callback_query']
            chat_id = callback_data['message']['chat']['id']
            callback_text = callback_data['data']
            message_id = callback_data['message']['message_id']
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": callback_data['id']}
            )
            
            # ОСНОВНЫЕ ОБРАБОТЧИКИ
            if callback_text == "menu_main":
                menu_data = menu_manager.get_main_menu()
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("menu_course_"):
                course_name = callback_text.replace("menu_course_", "")
                menu_data = menu_manager.get_enhanced_course_menu(course_name, chat_id)
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text == "menu_premium":
                menu_data = menu_manager.get_premium_menu()
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text == "menu_profile":
                menu_data = menu_manager.get_profile_menu(chat_id)
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text == "menu_development_fund":
                menu_data = menu_manager.get_development_fund_menu()
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            # ИНТЕРАКТИВНЫЕ УРОКИ
            elif callback_text.startswith('open_lesson_'):
                lesson_hash = callback_text.replace('open_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            user_level = USER_PROGRESS.get(chat_id, {}).get('уровень', 1)
                            menu_data = menu_manager.get_interactive_lesson(lesson, user_level)
                            update_lesson_state(chat_id, lesson, 0)
                            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('answer_'):
                # Обработка ответов пользователя
                parts = callback_text.split('_')
                if len(parts) >= 3:
                    user_answer_index = int(parts[1])
                    lesson_hash = int(parts[2])
                    
                    # Находим урок
                    for course_name, course_info in COURSES.items():
                        for lesson in course_info['уроки']:
                            if hash(lesson) == lesson_hash:
                                # Генерируем обратную связь (в реальности здесь должна быть логика проверки правильности)
                                # Пока считаем первый вариант правильным для демонстрации
                                correct_answer_index = 0
                                lesson_data = interactive_teacher.generate_interactive_lesson(lesson, 1)
                                
                                menu_data = menu_manager.get_lesson_feedback(
                                    user_answer_index, 
                                    correct_answer_index,
                                    lesson_data['explanation'],
                                    lesson
                                )
                                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                                break
                    return jsonify({"status": "ok"})
            
            elif callback_text.startswith('complete_lesson_'):
                lesson_hash = callback_text.replace('complete_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            update_user_progress(chat_id, lesson)
                            menu_data = menu_manager.get_enhanced_course_menu(course_name, chat_id)
                            success_text = f"✅ *Урок завершен!*\n\n🎯 Получено: 10 баллов\n📚 Урок: {lesson}\n\n💫 Ваш прогресс растет!\n\n{menu_data['text']}"
                            edit_main_message(chat_id, success_text, menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})

        # Обработка обычных сообщений
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if not chat_id:
            return jsonify({"status": "error", "message": "No chat_id"})

        if text == '/start':
            menu_data = menu_manager.get_main_menu()
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)