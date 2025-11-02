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
    }
}

USER_PROGRESS = {}  # {chat_id: {"пройденные_уроки": [], "уровень": 1, "баллы": 0}}
USER_MESSAGE_IDS = {}  # {chat_id: message_id} - для отслеживания основного сообщения
USER_LESSON_STATE = {}  # {chat_id: {"current_lesson": "", "step": 0, "conversation": []}}

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

# 🎯 ДИАЛОГОВЫЙ AI-ПРЕПОДАВАТЕЛЬ
class DialogAITeacher:
    def __init__(self):
        self.lesson_structures = {
            "beginner": ["объяснение", "вопрос", "практика", "обратная связь"],
            "intermediate": ["введение", "диалог", "кейс", "рефлексия"],
            "advanced": ["проблема", "анализ", "решение", "оптимизация"]
        }

    def generate_lesson_step(self, lesson_topic, user_level, conversation_history, current_step):
        """Генерирует следующий шаг урока на основе прогресса диалога"""
        
        system_prompt = f"""
        Ты - опытный AI-преподаватель. Веди урок в формате живого диалога с учеником.
        
        Тема урока: {lesson_topic}
        Уровень ученика: {user_level}/5
        Текущий этап: {current_step}
        
        История диалога:
        {self._format_conversation_history(conversation_history)}
        
        Сгенерируй следующий шаг урока. Структура:
        1. Твой ответ/вопрос (естественный, диалоговый)
        2. Тип взаимодействия (объяснение, вопрос, практика, обратная связь)
        3. Подсказки для продолжения (если нужны)
        
        Будь естественным, задавай открытые вопросы, адаптируйся под уровень ученика.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Продолжи урок, учитывая текущий прогресс:"}
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        return self._parse_dialog_response(response.choices[0].message.content)

    def _format_conversation_history(self, history):
        """Форматирует историю диалога для промпта"""
        if not history:
            return "Диалог только начинается"
        
        formatted = []
        for msg in history[-6:]:  # Берем последние 6 сообщений для контекста
            role = "Учитель" if msg["role"] == "teacher" else "Ученик"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)

    def _parse_dialog_response(self, text):
        """Парсит ответ AI на структурированные компоненты"""
        lines = text.split('\n')
        response_data = {
            "content": "",
            "interaction_type": "объяснение",
            "suggestions": [],
            "needs_input": True
        }
        
        current_section = "content"
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "тип:" in line.lower():
                response_data["interaction_type"] = line.split(":")[-1].strip()
            elif "подсказки:" in line.lower():
                current_section = "suggestions"
            elif current_section == "suggestions":
                if line.startswith(("-", "•", "*")):
                    response_data["suggestions"].append(line[1:].strip())
            else:
                if not response_data["content"]:
                    response_data["content"] = line
                else:
                    response_data["content"] += " " + line
        
        # Определяем нужен ли ввод от пользователя
        response_data["needs_input"] = any(word in response_data["content"].lower() for word in ["?", "расскажи", "объясни", "как", "почему"])
        
        return response_data

    def create_progress_tracker(self, completed_lessons, total_lessons=4):
        """Создает визуальный прогресс-бар"""
        progress_percent = (completed_lessons / total_lessons) * 100
        progress_bar = "🟩" * completed_lessons + "⬜" * (total_lessons - completed_lessons)
        
        achievements = []
        if completed_lessons >= 1:
            achievements.append("🎯 Начинающий")
        if completed_lessons >= 2:
            achievements.append("🚀 Практик") 
        if completed_lessons >= 4:
            achievements.append("🏆 Специалист")
            
        return {
            "progress_bar": f"{progress_bar} {progress_percent:.1f}%",
            "achievements": achievements,
            "completed": completed_lessons,
            "total": total_lessons
        }

# Инициализация преподавателя
dialog_teacher = DialogAITeacher()

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
        
        if len(USER_PROGRESS[chat_id]["пройденные_уроки"]) % 2 == 0:
            USER_PROGRESS[chat_id]["уровень"] += 1

def update_lesson_state(chat_id, lesson_name, step=0, user_message=None):
    """Обновляет состояние урока пользователя"""
    if chat_id not in USER_LESSON_STATE:
        USER_LESSON_STATE[chat_id] = {
            "current_lesson": lesson_name,
            "step": step,
            "conversation": []
        }
    
    # Добавляем сообщение пользователя в историю
    if user_message:
        USER_LESSON_STATE[chat_id]["conversation"].append({
            "role": "student",
            "content": user_message
        })
    
    USER_LESSON_STATE[chat_id]["step"] = step

def add_teacher_response(chat_id, teacher_message):
    """Добавляет ответ учителя в историю диалога"""
    if chat_id in USER_LESSON_STATE:
        USER_LESSON_STATE[chat_id]["conversation"].append({
            "role": "teacher",
            "content": teacher_message
        })

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
                    {"text": "💰 Премиум доступ", "callback_data": "menu_premium"},
                    {"text": "👤 Мой профиль", "callback_data": "menu_profile"}
                ],
                [
                    {"text": "🌍 Фонд развития", "callback_data": "menu_development_fund"}
                ]
            ]
        }
        
        text = """🧠 *NeuroTeacher*

*Твой AI-наставник в мире нейротехнологий*

Готов прокачать твой интеллект? Выбери направление:"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_enhanced_course_menu(self, course_name, user_id):
        """Возвращает улучшенное меню курса с прогрессом"""
        course_info = COURSES[course_name]
        progress = USER_PROGRESS.get(user_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
        
        progress_data = dialog_teacher.create_progress_tracker(
            len(progress['пройденные_уроки'])
        )
        
        lesson_buttons = []
        for i, lesson in enumerate(course_info['уроки']):
            status = "✅" if lesson in progress['пройденные_уроки'] else "📖"
            lesson_buttons.append([
                {"text": f"{status} Урок {i+1}: {lesson}", "callback_data": f"start_lesson_{hash(lesson)}"}
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

💫 *Выберите урок для начала:*"""
        
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

Откройте полный потенциал NeuroTeacher:

✅ Все курсы и уроки
🎓 Персональный AI-наставник 24/7
📊 Детальная аналитика прогресса
🔮 Эксклюзивные материалы

⚡ *Инвестиция в развитие: 10 TON/месяц*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_profile_menu(self, chat_id):
        """Возвращает меню профиля"""
        progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
            ]
        }
        
        text = f"""👤 *ВАШ ПРОФИЛЬ*

📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

🌍 *ФОНД РАЗВИТИЯ*
💫 Собрано в фонд: {DEVELOPMENT_FUND['development_fund']} TON
🚀 Всего доходов: {DEVELOPMENT_FUND['total_income']} TON

💫 *Продолжаем обучение!*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_development_fund_menu(self):
        """Возвращает меню Development Fund системы"""
        keyboard = {
            "inline_keyboard": [
                [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
            ]
        }
        
        text = f"""🌍 *СИСТЕМА DEVELOPMENT FUND*

💰 Всего доходов: {DEVELOPMENT_FUND['total_income']} TON
💫 Накоплено в фонд развития: {DEVELOPMENT_FUND['development_fund']} TON  
🚀 Маркетинг бюджет: {DEVELOPMENT_FUND['marketing_budget']} TON

📊 Распределение доходов:
• 70% - развитие платформы
• 20% - маркетинг и привлечение  
• 10% - основателю

⚡ *Создаем будущее образования вместе*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_dialog_lesson(self, chat_id, lesson_topic, user_input=None):
        """Возвращает диалоговый урок"""
        user_level = USER_PROGRESS.get(chat_id, {}).get('уровень', 1)
        lesson_state = USER_LESSON_STATE.get(chat_id, {})
        
        conversation_history = lesson_state.get("conversation", [])
        current_step = lesson_state.get("step", 0)
        
        # Генерируем следующий шаг урока
        lesson_step = dialog_teacher.generate_lesson_step(
            lesson_topic, 
            user_level, 
            conversation_history, 
            current_step
        )
        
        # Добавляем ответ учителя в историю
        add_teacher_response(chat_id, lesson_step["content"])
        
        # Обновляем шаг
        update_lesson_state(chat_id, lesson_topic, current_step + 1)
        
        # Создаем клавиатуру
        keyboard_buttons = []
        
        if lesson_step["suggestions"]:
            for suggestion in lesson_step["suggestions"][:3]:  # Максимум 3 подсказки
                keyboard_buttons.append([{"text": f"💡 {suggestion}", "callback_data": f"quick_reply_{hash(suggestion)}"}])
        
        if lesson_step["needs_input"]:
            keyboard_buttons.append([{"text": "✏️ Написать ответ", "callback_data": "waiting_input"}])
        
        keyboard_buttons.extend([
            [{"text": "✅ Завершить урок", "callback_data": f"complete_lesson_{hash(lesson_topic)}"}],
            [{"text": "🔄 Начать заново", "callback_data": f"restart_lesson_{hash(lesson_topic)}"}],
            [{"text": "🔙 Назад к курсу", "callback_data": "menu_course_back"}]
        ])
        
        keyboard = {"inline_keyboard": keyboard_buttons}
        
        # Форматируем текст
        interaction_icon = {
            "объяснение": "🧠",
            "вопрос": "❓", 
            "практика": "🔧",
            "обратная связь": "💫",
            "диалог": "💬"
        }.get(lesson_step["interaction_type"], "💬")
        
        text = f"""{interaction_icon} *{lesson_topic}*

{lesson_step['content']}

📝 *Тип:* {lesson_step['interaction_type'].title()}"""
        
        return {"text": text, "keyboard": keyboard, "needs_input": lesson_step["needs_input"]}

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
        "status": "NeuroTeacher - Dialog Education Platform",
        "version": "4.0", 
        "ready": True,
        "founder_wallet": TON_WALLET
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "NeuroTeacher"})

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
            
            # ОСНОВНЫЕ ОБРАБОТЧИКИ МЕНЮ
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
            
            # ДИАЛОГОВЫЕ УРОКИ
            elif callback_text.startswith('start_lesson_'):
                lesson_hash = callback_text.replace('start_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            # Начинаем новый урок
                            update_lesson_state(chat_id, lesson, 0)
                            menu_data = menu_manager.get_dialog_lesson(chat_id, lesson)
                            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('quick_reply_'):
                # Быстрый ответ через кнопку
                suggestion_hash = callback_text.replace('quick_reply_', '')
                lesson_state = USER_LESSON_STATE.get(chat_id, {})
                current_lesson = lesson_state.get("current_lesson", "")
                
                if current_lesson:
                    # Находим текст подсказки по хешу
                    for course_name, course_info in COURSES.items():
                        for lesson in course_info['уроки']:
                            if lesson == current_lesson:
                                # Используем подсказку как ответ пользователя
                                update_lesson_state(chat_id, current_lesson, lesson_state["step"], "Использую подсказку")
                                menu_data = menu_manager.get_dialog_lesson(chat_id, current_lesson, "Использую подсказку")
                                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                                break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('complete_lesson_'):
                lesson_hash = callback_text.replace('complete_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            update_user_progress(chat_id, lesson)
                            # Очищаем состояние урока
                            if chat_id in USER_LESSON_STATE:
                                del USER_LESSON_STATE[chat_id]
                            
                            menu_data = menu_manager.get_enhanced_course_menu(course_name, chat_id)
                            success_text = f"""🎉 *Урок завершен!*

📚 Тема: {lesson}
🎯 Получено: 10 баллов
💫 Уровень повышен!

{menu_data['text']}"""
                            
                            edit_main_message(chat_id, success_text, menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('restart_lesson_'):
                lesson_hash = callback_text.replace('restart_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            # Начинаем урок заново
                            update_lesson_state(chat_id, lesson, 0)
                            menu_data = menu_manager.get_dialog_lesson(chat_id, lesson)
                            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})

        # ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ (диалог)
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if not chat_id:
            return jsonify({"status": "error", "message": "No chat_id"})

        # Команда /start
        if text == '/start':
            menu_data = menu_manager.get_main_menu()
            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'])
            return jsonify({"status": "ok"})
        
        # Обработка текстовых ответов в уроках
        lesson_state = USER_LESSON_STATE.get(chat_id, {})
        if lesson_state and "current_lesson" in lesson_state:
            current_lesson = lesson_state["current_lesson"]
            
            # Обновляем состояние с ответом пользователя
            update_lesson_state(chat_id, current_lesson, lesson_state["step"], text)
            
            # Получаем следующий шаг урока
            menu_data = menu_manager.get_dialog_lesson(chat_id, current_lesson, text)
            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], USER_MESSAGE_IDS.get(chat_id))
            
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)