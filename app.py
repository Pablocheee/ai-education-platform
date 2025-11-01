from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging
import time
from datetime import datetime

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

USER_PROGRESS = {}
USER_SESSIONS = {}

UBI_SYSTEM = {
    "total_income": 0,
    "ubi_fund": 0,
    "distributed": 0,
    "transactions": []
}

class SmartLearningSystem:
    """Умная система адаптивного обучения"""
    
    def __init__(self):
        self.learning_formats = {
            "micro": {
                "duration": "5-7 минут",
                "structure": "1 ключевая идея + практическое применение",
                "best_for": ["утро", "обед", "мобильные устройства"]
            },
            "standard": {
                "duration": "15-20 минут", 
                "structure": "теория + практика + задание",
                "best_for": ["вечер", "пк", "глубокое погружение"]
            },
            "deep_dive": {
                "duration": "30-45 минут",
                "structure": "расширенная теория + кейсы + проект",
                "best_for": ["выходные", "погружение", "проектная работа"]
            }
        }
    
    def detect_optimal_format(self, user_id, context=None):
        """Определяет оптимальный формат обучения для пользователя"""
        user_session = USER_SESSIONS.get(user_id, {})
        
        # Анализ времени суток
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 9:  # Утро
            time_context = "утро"
        elif 12 <= current_hour <= 14:  # Обед
            time_context = "обед" 
        elif 18 <= current_hour <= 22:  # Вечер
            time_context = "вечер"
        else:
            time_context = "стандарт"
        
        # Анализ истории обучения
        user_progress = USER_PROGRESS.get(user_id, {})
        completed_lessons = len(user_progress.get("пройденные_уроки", []))
        
        if completed_lessons < 3:
            return "micro"  # Новым пользователям - микро-формат
        elif time_context in ["утро", "обед"]:
            return "micro"
        elif time_context == "вечер" and completed_lessons > 5:
            return "deep_dive"
        else:
            return "standard"
    
    def generate_adaptive_lesson(self, lesson_topic, user_id):
        """Генерирует адаптивный урок на основе формата"""
        optimal_format = self.detect_optimal_format(user_id)
        user_level = USER_PROGRESS.get(user_id, {}).get("уровень", 1)
        
        format_prompts = {
            "micro": f"""
            Создай МИКРО-урок (5-7 минут) на тему: "{lesson_topic}"
            
            Структура:
            🎯 ОДНА ключевая идея (самое важное)
            💡 Практическое применение (3 конкретных шага)
            🚀 Быстрый результат (что получит прямо сейчас)
            
            Требования:
            - Максимально практично
            - Можно применить сразу после урока
            - Язык: простой и понятный
            """,
            
            "standard": f"""
            Создай СТАНДАРТНЫЙ урок (15-20 минут) на тему: "{lesson_topic}"
            
            Структура:
            1. 📚 Теоретическая основа (понятным языком)
            2. 🔧 Практическое применение с примерами
            3. 🎯 Задание для закрепления
            4. 💫 Советы для дальнейшего развития
            
            Уровень сложности: {user_level}/5
            """,
            
            "deep_dive": f"""
            Создай УГЛУБЛЕННЫЙ урок (30-45 минут) на тему: "{lesson_topic}"
            
            Структура:
            🌟 Расширенная теория с кейсами
            🔬 Детальный разбор механизмов работы  
            🛠️ Практический проект или задание
            📈 Метрики успеха и прогресса
            🎯 Рекомендации для экспертного уровня
            
            Уровень: продвинутый ({user_level}/5)
            """
        }
        
        prompt = format_prompts.get(optimal_format, format_prompts["standard"])
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты эксперт-преподаватель с 20-летним опытом. Создавай практические, полезные уроки которые сразу можно применять в работе."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            lesson_content = response.choices[0].message.content
            return f"📚 *Формат: {optimal_format.upper()}*\n\n{lesson_content}"
            
        except Exception as e:
            return f"📚 *{lesson_topic}*\n\nПоказываю базовый урок. Система AI временно недоступна."

class GamificationSystem:
    """Система геймификации и мотивации"""
    
    def __init__(self):
        self.achievements = {
            "first_lesson": {"name": "🎯 Первый шаг", "points": 10},
            "fast_learner": {"name": "⚡ Быстрый ученик", "points": 20},
            "course_completed": {"name": "🏆 Завершил курс", "points": 50},
            "consistent_learner": {"name": "📅 Постоянный ученик", "points": 30}
        }
    
    def check_achievements(self, user_id):
        """Проверяет и выдает достижения"""
        progress = USER_PROGRESS.get(user_id, {})
        completed = progress.get("пройденные_уроки", [])
        points = progress.get("баллы", 0)
        
        new_achievements = []
        
        # Проверка достижений
        if len(completed) == 1 and "first_lesson" not in progress.get("achievements", []):
            new_achievements.append(self.achievements["first_lesson"])
        
        if len(completed) >= 3 and "fast_learner" not in progress.get("achievements", []):
            new_achievements.append(self.achievements["fast_learner"])
            
        if points >= 100 and "consistent_learner" not in progress.get("achievements", []):
            new_achievements.append(self.achievements["consistent_learner"])
        
        # Добавляем достижения в прогресс
        if new_achievements:
            if "achievements" not in progress:
                progress["achievements"] = []
            
            for achievement in new_achievements:
                progress["achievements"].append(achievement["name"])
                progress["баллы"] += achievement["points"]
            
            USER_PROGRESS[user_id] = progress
            
        return new_achievements

# Инициализация систем
smart_learning = SmartLearningSystem()
gamification = GamificationSystem()

def update_user_progress(chat_id, lesson_name):
    """Обновляет прогресс пользователя"""
    if chat_id not in USER_PROGRESS:
        USER_PROGRESS[chat_id] = {
            "пройденные_уроки": [], 
            "уровень": 1, 
            "баллы": 0,
            "achievements": [],
            "last_active": datetime.now().isoformat()
        }
    
    if lesson_name not in USER_PROGRESS[chat_id]["пройденные_уроки"]:
        USER_PROGRESS[chat_id]["пройденные_уроки"].append(lesson_name)
        USER_PROGRESS[chat_id]["баллы"] += 10
        USER_PROGRESS[chat_id]["last_active"] = datetime.now().isoformat()
        
        # Повышение уровня каждые 4 урока
        if len(USER_PROGRESS[chat_id]["пройденные_уроки"]) % 4 == 0:
            USER_PROGRESS[chat_id]["уровень"] += 1
            
        # Проверка достижений
        gamification.check_achievements(chat_id)

def process_ubi_payment(amount, from_user):
    """Обрабатывает платеж и распределяет по UBI"""
    UBI_SYSTEM["total_income"] += amount
    
    distribution = {
        "reinvestment": amount * 0.6,      # 60% на развитие
        "ubi_fund": amount * 0.3,          # 30% в UBI фонд  
        "founder": amount * 0.1            # 10% основателю
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

def generate_ton_payment_link(chat_id, amount=10):
    """Генерирует платежную ссылку для Tonkeeper"""
    return f"https://app.tonkeeper.com/transfer/{TON_WALLET}?amount={amount*1000000000}&text=premium_{chat_id}"

@app.route('/')
def home():
    return jsonify({
        "status": "AI Education Platform - UBI Concept",
        "version": "3.0", 
        "ready": True,
        "founder_wallet": TON_WALLET,
        "active_users": len(USER_PROGRESS),
        "ubi_fund": UBI_SYSTEM["ubi_fund"]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "AI Teacher", "timestamp": datetime.now().isoformat()})

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    """Webhook для Telegram бота"""
    try:
        data = request.json
        print(f"📨 Received: {data}")  # Логируем входящие данные

        # Обработка callback_query
        if 'callback_query' in data:
            callback_data = data['callback_query']
            chat_id = callback_data['message']['chat']['id']
            callback_text = callback_data['data']
            
            # Отвечаем на callback чтобы убрать "часики"
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": callback_data['id']}
            )
            
            if callback_text.startswith('complete_'):
                lesson_hash = callback_text.replace('complete_', '')
                
                # Находим название урока по хешу
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if str(hash(lesson)) == lesson_hash:
                            update_user_progress(chat_id, lesson)
                            
                            # Проверяем достижения
                            new_achievements = gamification.check_achievements(chat_id)
                            
                            achievement_text = ""
                            if new_achievements:
                                achievement_text = "\n\n🎉 Новые достижения:\n" + "\n".join([f"• {ach['name']} (+{ach['points']} баллов)" for ach in new_achievements])
                            
                            response_text = f"✅ *Урок отмечен пройденным!*\n\n🎯 Получено: 10 баллов\n📚 Урок: {lesson}{achievement_text}"
                            
                            requests.post(
                                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                                json={
                                    "chat_id": chat_id,
                                    "text": response_text,
                                    "parse_mode": "Markdown"
                                }
                            )
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('open_lesson_'):
                lesson_hash = callback_text.replace('open_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if str(hash(lesson)) == lesson_hash:
                            # Генерируем адаптивный AI-урок
                            ai_lesson = smart_learning.generate_adaptive_lesson(lesson, chat_id)
                            
                            # Отправляем урок с кнопкой "✅ Завершить урок"
                            inline_keyboard = {
                                "inline_keyboard": [[
                                    {"text": "✅ Завершить урок", "callback_data": f"complete_{lesson_hash}"}
                                ]]
                            }
                            
                            requests.post(
                                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                                json={
                                    "chat_id": chat_id,
                                    "text": ai_lesson,
                                    "parse_mode": "Markdown",
                                    "reply_markup": inline_keyboard
                                }
                            )
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text == "show_progress":
                progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
                achievements = progress.get("achievements", [])
                
                achievements_text = "\n".join(achievements) if achievements else "🎯 Пока нет достижений"
                
                response_text = f"""📊 *ВАШ ПРОГРЕСС*

🎯 Уровень: {progress['уровень']}
⭐ Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

🏆 Достижения:
{achievements_text}

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

        # Обработка обычных сообщений
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if not chat_id:
            return jsonify({"status": "error", "message": "No chat_id"})

        # Обработка команды /start
        if text == '/start':
            keyboard = {
                "keyboard": [
                    ["🚀 Войти в систему AI", "💫 Запустить эволюцию"],
                    ["🌌 База знаний", "⚡ Карьерный ускоритель"],
                    ["💰 Премиум доступ", "👤 Мой профиль"],
                    ["🌍 UBI Система"]
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
        elif text in COURSES.keys():
            course_info = COURSES[text]
            response_text = f"*{text}*\n\n{course_info['описание']}\n\n*Уровень:* {course_info['уровень']}\n\n*Модули:*\n" + "\n".join([f"• {lesson}" for lesson in course_info['уроки']])
            
            # Создаем инлайн-кнопки для каждого урока
            inline_keyboard = {
                "inline_keyboard": [
                    [{"text": f"📖 {lesson}", "callback_data": f"open_lesson_{hash(lesson)}"}]
                    for lesson in course_info['уроки']
                ]
            }
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": response_text,
                    "reply_markup": inline_keyboard,
                    "parse_mode": "Markdown"
                }
            )
            
        elif text == "💰 Премиум доступ":
            payment_link = generate_ton_payment_link(chat_id)
            
            inline_keyboard = {
                "inline_keyboard": [[
                    {
                        "text": "💳 Активировать полный доступ", 
                        "url": payment_link
                    }
                ]]
            }
            
            response_text = """💰 *ПРЕМИУМ ДОСТУП*

Откройте полный потенциал системы:

✅ Все модули и архивы знаний
🎓 Персональный AI-наставник 24/7
📊 Система отслеживания прогресса  
🔮 Эксклюзивные материалы будущего

*Инвестиция в вашу эволюцию: 10 TON/месяц*"""
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": response_text,
                    "reply_markup": inline_keyboard,
                    "parse_mode": "Markdown"
                }
            )
            
        elif text == "👤 Мой профиль":
            progress = USER_PROGRESS.get(chat_id, {"пройденные_уроки": [], "уровень": 1, "баллы": 0})
            achievements = progress.get("achievements", [])
            
            achievements_text = "\n".join([f"• {ach}" for ach in achievements]) if achievements else "• 🎯 Пока нет достижений"
            
            response_text = f"""👤 *ВАШ ПРОФИЛЬ В СИСТЕМЕ*

📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

🏆 Достижения:
{achievements_text}

🌍 *UBI СИСТЕМА*
💫 Собрано в фонд: {UBI_SYSTEM['ubi_fund']} TON
🚀 Всего доходов: {UBI_SYSTEM['total_income']} TON

💫 *Эволюция продолжается...*"""

            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": response_text,
                    "parse_mode": "Markdown"
                }
            )

        elif text == "🌍 UBI Система":
            response_text = f"""🌍 *СИСТЕМА UBI FUTURE_UBI*

💰 Всего доходов: {UBI_SYSTEM['total_income']} TON
💫 Накоплено в UBI фонд: {UBI_SYSTEM['ubi_fund']} TON  
🚀 Распределено: {UBI_SYSTEM['distributed']} TON

📊 Распределение доходов:
• 60% - развитие платформы
• 30% - UBI фонд для сообщества  
• 10% - основателю за создание

💫 *Создаем экономику изобилия вместе*"""

            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": response_text,
                    "parse_mode": "Markdown"
                }
            )

        # Обработка обычных сообщений через AI
        elif text and not text.startswith('/'):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Ты AI-преподаватель в образовательной платформе. Отвечай полезно и понятно на русском. Будь практичным и мотивирующим."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=500
                )
                
                ai_response = response.choices[0].message.content
                
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"💡 *AI-преподаватель:*\n\n{ai_response}",
                        "parse_mode": "Markdown"
                    }
                )
                
            except Exception as e:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "⚠️ Система AI временно недоступна. Попробуйте позже."
                    }
                )

        return jsonify({"status": "ok"})
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/ton-payment-webhook', methods=['POST'])
def ton_payment_webhook():
    """Вебхук для подтверждения платежей TON"""
    try:
        data = request.json
        print(f"💰 Получен платеж: {data}")
        
        # Тестовая реализация - при первом вызове добавляем тестовый платеж
        if UBI_SYSTEM["total_income"] == 0:
            distribution = process_ubi_payment(10, "first_test_payment")
            return jsonify({
                "status": "success", 
                "distribution": distribution,
                "message": f"💰 Тестовый платеж обработан! UBI фонд пополнен на {distribution['ubi_fund']} TON"
            })
            
        # Реальная обработка платежа
        if data.get('status') == 'success':
            amount = data.get('amount', 0)
            from_user = data.get('from', 'unknown')
            chat_id = data.get('chat_id')
            
            distribution = process_ubi_payment(amount, from_user)
            
            if chat_id:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"✅ *Платеж получен!*\n\nСпасибо за поддержку UBI системы!\n\n💫 Распределение:\n• {distribution['reinvestment']} TON - развитие\n• {distribution['ubi_fund']} TON - UBI фонд\n• {distribution['founder']} TON - основателю",
                        "parse_mode": "Markdown"
                    }
                )
            
            return jsonify({"status": "success", "processed": True})
        else:
            return jsonify({"status": "pending"})
            
    except Exception as e:
        logging.error(f"Payment error: {e}")
        return jsonify({"status": "error"})

@app.route('/test-payment/<chat_id>', methods=['GET'])
def test_payment(chat_id):
    """Тестовый платеж для отладки"""
    distribution = process_ubi_payment(10, f"test_user_{chat_id}")
    
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
        json={
            "chat_id": chat_id,
            "text": f"🧪 *Тестовый платеж обработан!*\n\nРаспределение UBI:\n• {distribution['reinvestment']} TON - развитие\n• {distribution['ubi_fund']} TON - UBI фонд\n• {distribution['founder']} TON - основателю\n\n💫 Система готова к реальным платежам!",
            "parse_mode": "Markdown"
        }
    )
    
    return jsonify({"status": "test_payment_processed", "distribution": distribution})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Статистика системы"""
    return jsonify({
        "active_users": len(USER_PROGRESS),
        "total_lessons_completed": sum(len(user.get("пройденные_уроки", [])) for user in USER_PROGRESS.values()),
        "ubi_system": UBI_SYSTEM,
        "courses_available": len(COURSES),
        "total_lessons": sum(len(course["уроки"]) for course in COURSES.values())
    })

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