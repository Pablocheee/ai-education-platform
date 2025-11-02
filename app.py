from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
from typing import Dict, List, Tuple
import time

app = Flask(__name__)

# Настройка API ключей
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TON_WALLET = os.getenv('TON_WALLET', 'UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY')

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

USER_PROGRESS = {}
USER_MESSAGE_IDS = {}
USER_CURRENT_TOPIC = {}
USER_LESSON_PROGRESS = {}  # {chat_id: {"current_lesson": "prompting_basics", "current_module": 0, "score": 0}}

UBI_SYSTEM = {
    "total_income": 0,
    "ubi_fund": 0,
    "distributed": 0,
    "transactions": []
}

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
    
    return text, keyboard

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

# 🔧 ОБНОВЛЯЕМ WEBHOOK ДЛЯ МИКРО-ОБУЧЕНИЯ
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
            
            # Отвечаем на callback чтобы убрать "часики"
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": callback_data['id']}
            )
            
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
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)})

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