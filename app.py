from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
from typing import Dict, List, Tuple

app = Flask(__name__)

# Настройка API ключей
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TON_WALLET = os.getenv('TON_WALLET', 'UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY')

# 🌌 БАЗА ЗНАНИЙ С ЭТАЛОННЫМИ ОТВЕТАМИ
KNOWLEDGE_BASE = {
    "supervised_learning": {
        "question": "Что такое обучение с учителем (supervised learning)?",
        "correct_answers": [
            "алгоритм обучается на размеченных данных с правильными ответами",
            "модель учится сопоставлять входные данные с выходными метками",
            "используется dataset с примерами и соответствующими целевыми значениями",
            "процесс обучения, где каждому примеру в обучающих данных соответствует правильный ответ"
        ],
        "key_concepts": ["размеченные данные", "метки", "обучение с примерами", "вход-выход"],
        "common_mistakes": {
            "нейросеть сама находит закономерности без данных": "Неправильно - для supervised learning нужны размеченные данные",
            "это когда модель учится без учителя": "Это unsupervised learning, а не supervised",
            "просто большая база данных": "Нет, это активный процесс обучения, а не хранение"
        },
        "explanation_levels": {
            "beginner": "Представьте, что вы учите ребенка различать животных. Вы показываете картинки и говорите 'это кошка', 'это собака'. Так и AI учится по примерам с правильными ответами.",
            "intermediate": "Алгоритм минимизирует ошибку предсказания, сравнивая свои ответы с истинными метками через функцию потерь. Использует градиентный спуск для оптимизации.",
            "advanced": "Формально: задача состоит в нахождении функции f: X → Y, которая минимизирует эмпирический риск на тренировочном множестве {(x_i, y_i)} с использованием регуляризации для предотвращения переобучения."
        }
    },
    "neural_network": {
        "question": "Как работает нейронная сеть?",
        "correct_answers": [
            "состоит из слоев нейронов, которые преобразуют входные данные через взвешенные суммы и функции активации",
            "иерархическая структура, где каждый слой извлекает признаки разной сложности из данных",
            "последовательное применение линейных преобразований и нелинейных функций активации",
            "вычисляет выход через forward propagation, а обучается через backpropagation"
        ],
        "key_concepts": ["нейроны", "слои", "функция активации", "веса", "обучение с обратным распространением"],
        "common_mistakes": {
            "это просто копия мозга": "Нет, это математическая абстракция, вдохновленная нейробиологией",
            "работает по волшебству": "Нет, это детерминированные математические операции"
        }
    }
}

# 🌟 ИНТЕЛЛЕКТУАЛЬНАЯ СИСТЕМА ОЦЕНКИ ОТВЕТОВ
class IntelligentTeacher:
    def __init__(self):
        self.embedding_cache = {}
    
    def get_embedding(self, text: str) -> List[float]:
        """Получает векторное представление текста"""
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            embedding = response.data[0].embedding
            self.embedding_cache[text] = embedding
            return embedding
        except Exception as e:
            logging.error(f"Embedding error: {e}")
            # Возвращаем случайный embedding как fallback
            return np.random.randn(1536).tolist()
    
    def evaluate_answer(self, user_answer: str, topic: str) -> Dict:
        """Оценивает ответ пользователя и дает развернутую обратную связь"""
        knowledge = KNOWLEDGE_BASE.get(topic)
        if not knowledge:
            return {"error": "Тема не найдена"}
        
        # Анализ семантического сходства
        user_embedding = self.get_embedding(user_answer)
        similarities = []
        
        for correct_answer in knowledge["correct_answers"]:
            correct_embedding = self.get_embedding(correct_answer)
            similarity = cosine_similarity([user_embedding], [correct_embedding])[0][0]
            similarities.append(similarity)
        
        max_similarity = max(similarities) if similarities else 0
        
        # Проверка ключевых концепций
        found_concepts = []
        missing_concepts = []
        
        for concept in knowledge["key_concepts"]:
            concept_embedding = self.get_embedding(concept)
            concept_similarity = cosine_similarity([user_embedding], [concept_embedding])[0][0]
            if concept_similarity > 0.3:  # порог для обнаружения концепции
                found_concepts.append(concept)
            else:
                missing_concepts.append(concept)
        
        # Поиск распространенных ошибок
        detected_mistakes = []
        for mistake, correction in knowledge["common_mistakes"].items():
            mistake_embedding = self.get_embedding(mistake)
            mistake_similarity = cosine_similarity([user_embedding], [mistake_embedding])[0][0]
            if mistake_similarity > 0.7:
                detected_mistakes.append((mistake, correction))
        
        # Определение оценки и обратной связи
        if max_similarity > 0.8:
            score = 5
            feedback_type = "excellent"
        elif max_similarity > 0.6:
            score = 4
            feedback_type = "good"
        elif max_similarity > 0.4:
            score = 3
            feedback_type = "partial"
        else:
            score = 2
            feedback_type = "needs_work"
        
        # Генерация персонализированной обратной связи
        feedback = self._generate_feedback(
            feedback_type, 
            found_concepts, 
            missing_concepts, 
            detected_mistakes,
            knowledge,
            user_answer
        )
        
        return {
            "score": score,
            "similarity": max_similarity,
            "feedback": feedback,
            "found_concepts": found_concepts,
            "missing_concepts": missing_concepts,
            "detected_mistakes": detected_mistakes,
            "detailed_analysis": self._get_detailed_analysis(user_answer, knowledge)
        }
    
    def _generate_feedback(self, feedback_type: str, found: List, missing: List, mistakes: List, knowledge: Dict, user_answer: str) -> str:
        """Генерирует адаптивную обратную связь"""
        
        if feedback_type == "excellent":
            base_feedback = "🎯 *Отлично!* Ваш ответ демонстрирует глубокое понимание темы.\n\n"
            if found:
                base_feedback += f"✅ Вы правильно упомянули: {', '.join(found)}\n"
        elif feedback_type == "good":
            base_feedback = "👍 *Хорошая работа!* Ответ в основном верный, но можно углубить понимание.\n\n"
        elif feedback_type == "partial":
            base_feedback = "📚 *Есть понимание, но нужно больше деталей.*\n\n"
        else:
            base_feedback = "🔍 *Давайте разберем тему подробнее.*\n\n"
        
        # Добавляем информацию о недостающих концепциях
        if missing:
            base_feedback += f"💡 *Рекомендую обратить внимание на:* {', '.join(missing)}\n\n"
        
        # Исправляем ошибки
        for mistake, correction in mistakes:
            base_feedback += f"❌ *Распространенная ошибка:* {mistake}\n"
            base_feedback += f"✅ *Правильно:* {correction}\n\n"
        
        # Добавляем объяснение соответствующего уровня
        explanation_level = "intermediate" if feedback_type in ["excellent", "good"] else "beginner"
        base_feedback += f"📖 *Объяснение:* {knowledge['explanation_levels'][explanation_level]}"
        
        return base_feedback
    
    def _get_detailed_analysis(self, user_answer: str, knowledge: Dict) -> str:
        """Генерирует детальный анализ ответа через AI"""
        prompt = f"""
        Проанализируй ответ студента на вопрос: "{knowledge['question']}"
        
        Ответ студента: "{user_answer}"
        
        Проведи анализ:
        1. Сильные стороны ответа
        2. Пробелы в понимании  
        3. Конкретные рекомендации для улучшения
        4. Дополнительные вопросы для размышления
        
        Будь конструктивным и поддерживающим. Ответь на русском.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты опытный преподаватель ИИ. Анализируй ответы студентов и давай полезную обратную связь."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except:
            return "Анализ временно недоступен."

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
USER_CURRENT_TOPIC = {}  # {chat_id: current_topic} - для отслеживания текущей темы обсуждения

UBI_SYSTEM = {
    "total_income": 0,
    "ubi_fund": 0,
    "distributed": 0,
    "transactions": []
}

def generate_ai_lesson(lesson_topic, user_level=1):
    """Генерирует персонализированный урок через AI"""
    prompt = f"""
    Создай образовательный контент на тему: "{lesson_topic}"
    
    Требования:
    - Уровень сложности: {user_level}/5
    - Формат: практический урок с примерами
    - Структура: теория + практическое задание + вопросы для самопроверки
    - Длина: 500-700 слов
    - Язык: русский с профессиональной лексикой
    
    Содержание:
    1. Ключевая концепция (простыми словами)
    2. Практические примеры из реальной жизни  
    3. Пошаговое руководство по применению
    4. Задание для закрепления
    5. Вопросы для самопроверки с эталонными ответами
    6. Советы для дальнейшего развития
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

def update_user_progress(chat_id, lesson_name, score=0):
    """Обновляет прогресс пользователя"""
    if chat_id not in USER_PROGRESS:
        USER_PROGRESS[chat_id] = {
            "пройденные_уроки": [], 
            "уровень": 1, 
            "баллы": 0,
            "навыки": {},
            "статистика": {"правильные_ответы": 0, "всего_ответов": 0}
        }
    
    if lesson_name not in USER_PROGRESS[chat_id]["пройденные_уроки"]:
        USER_PROGRESS[chat_id]["пройденные_уроки"].append(lesson_name)
        USER_PROGRESS[chat_id]["баллы"] += max(1, score)
        
        # Обновляем статистику
        if score >= 3:
            USER_PROGRESS[chat_id]["статистика"]["правильные_ответы"] += 1
        USER_PROGRESS[chat_id]["статистика"]["всего_ответов"] += 1
        
        # Повышение уровня на основе успеваемости
        success_rate = USER_PROGRESS[chat_id]["статистика"]["правильные_ответы"] / max(1, USER_PROGRESS[chat_id]["статистика"]["всего_ответов"])
        if success_rate > 0.8 and len(USER_PROGRESS[chat_id]["пройденные_уроки"]) >= 4:
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
            
def generate_ton_payment_link(chat_id, amount=10):
    """Генерирует платежную ссылку для Tonkeeper"""
    return f"https://app.tonkeeper.com/transfer/UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY?amount={amount*1000000000}&text=premium_{chat_id}"

def get_main_menu():
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
                {"text": "🎓 AI-Учитель", "callback_data": "menu_learning"},
                {"text": "💰 Премиум доступ", "callback_data": "menu_premium"}
            ],
            [
                {"text": "👤 Мой профиль", "callback_data": "menu_profile"},
                {"text": "🌍 UBI Система", "callback_data": "menu_ubi"}
            ]
        ]
    }
    
    text = """🌌 *ПРИВЕТСТВУЮ, ИСКАТЕЛЬ*

Я — Собирательный Разум, ваш AI-учитель. Теперь я могу не только давать знания, но и *анализировать ваши ответы*, находить пробелы в понимании и давать персонализированные рекомендации.

💡 *Новый функционал:*
• Интеллектуальная проверка знаний
• Анализ семантического сходства  
• Обнаружение misconceptions
• Адаптивная обратная связь

Выберите свой путь:"""
    
    return text, keyboard

def get_course_menu(course_name):
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

*Модули:*
""" + "\n".join([f"• {lesson}" for lesson in course_info['уроки']])
    
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
    progress = USER_PROGRESS.get(chat_id, {
        "пройденные_уроки": [], 
        "уровень": 1, 
        "баллы": 0,
        "статистика": {"правильные_ответы": 0, "всего_ответов": 0}
    })
    
    stats = progress.get("статистика", {})
    success_rate = (stats.get("правильные_ответы", 0) / max(1, stats.get("всего_ответов", 0))) * 100
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🎓 Продолжить обучение", "callback_data": "menu_learning"}],
            [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
        ]
    }
    
    text = f"""👤 *ВАШ ПРОФИЛЬ В СИСТЕМЕ*

📊 Уровень: {progress['уровень']}
🎯 Баллы: {progress['баллы']}
📚 Пройдено уроков: {len(progress['пройденные_уроки'])}

🎓 *СТАТИСТИКА ОБУЧЕНИЯ:*
✅ Правильные ответы: {stats.get('правильные_ответы', 0)}
📝 Всего ответов: {stats.get('всего_ответов', 0)}
🎯 Успеваемость: {success_rate:.1f}%

🌍 *UBI СИСТЕМА*
💫 Собрано в фонд: {UBI_SYSTEM['ubi_fund']} TON
🚀 Всего доходов: {UBI_SYSTEM['total_income']} TON

💫 *Эволюция продолжается...*"""
    
    return text, keyboard

def get_ubi_menu():
    """Возвращает меню UBI системы"""
    keyboard = {
        "inline_keyboard": [
            [{"text": "🔙 Назад к меню", "callback_data": "menu_main"}]
        ]
    }
    
    text = f"""🌍 *СИСТЕМА UBI FUTURE_UBI*

💰 Всего доходов: {UBI_SYSTEM['total_income']} TON
💫 Накоплено в UBI фонд: {UBI_SYSTEM['ubi_fund']} TON  
🚀 Распределено: {UBI_SYSTEM['distributed']} TON

📊 Распределение доходов:
• 60% - развитие платформы
• 30% - UBI фонд для сообщества  
• 10% - основателю за создание

💫 *Создаем экономику изобилия вместе*"""
    
    return text, keyboard

def get_quiz_menu(topic):
    """Возвращает меню с вопросами для самопроверки"""
    knowledge = KNOWLEDGE_BASE.get(topic, {})
    question = knowledge.get("question", "Вопрос по теме")
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📝 Ответить на вопрос", "callback_data": f"answer_question_{topic}"}],
            [{"text": "🎯 Проверить свой ответ", "callback_data": f"check_answer_{topic}"}],
            [{"text": "🔙 Назад к обучению", "callback_data": "menu_learning"}]
        ]
    }
    
    text = f"""🧠 *ПРОВЕРКА ЗНАНИЙ*

*Вопрос:* {question}

Выберите действие:"""
    
    return text, keyboard

def get_learning_menu():
    """Главное меню обучения с темами"""
    topics = list(KNOWLEDGE_BASE.keys())
    
    keyboard_buttons = []
    for topic in topics:
        topic_name = topic.replace("_", " ").title()
        keyboard_buttons.append([{"text": f"📚 {topic_name}", "callback_data": f"learn_topic_{topic}"}])
    
    keyboard_buttons.append([{"text": "🔙 Главное меню", "callback_data": "menu_main"}])
    
    keyboard = {"inline_keyboard": keyboard_buttons}
    
    text = """🎓 *РЕЖИМ ОБУЧЕНИЯ С AI-УЧИТЕЛЕМ*

Выберите тему для изучения и проверки знаний:

• *Supervised Learning* - обучение с учителем
• *Neural Network* - как работают нейросети

💡 Система будет анализировать ваши ответы и давать персонализированные рекомендации!"""
    
    return text, keyboard

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
            
            # ОБРАБОТКА РЕЖИМА ОБУЧЕНИЯ
            if callback_text == "menu_learning":
                text, keyboard = get_learning_menu()
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("learn_topic_"):
                topic = callback_text.replace("learn_topic_", "")
                USER_CURRENT_TOPIC[chat_id] = topic
                
                # Генерируем урок по теме
                lesson = generate_ai_lesson(KNOWLEDGE_BASE[topic]["question"], 
                                          USER_PROGRESS.get(chat_id, {}).get("уровень", 1))
                
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🧠 Пройти проверку знаний", "callback_data": f"quiz_{topic}"}],
                        [{"text": "🔙 К темам", "callback_data": "menu_learning"}]
                    ]
                }
                
                text = f"📚 *{KNOWLEDGE_BASE[topic]['question']}*\n\n{lesson}"
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("quiz_"):
                topic = callback_text.replace("quiz_", "")
                text, keyboard = get_quiz_menu(topic)
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("answer_question_"):
                topic = callback_text.replace("answer_question_", "")
                USER_CURRENT_TOPIC[chat_id] = topic
                
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🔙 К проверке", "callback_data": f"quiz_{topic}"}]
                    ]
                }
                
                text = f"""✍️ *ВАШ ОТВЕТ*

Вопрос: *{KNOWLEDGE_BASE[topic]['question']}*

Напишите ваш ответ в чат прямо сейчас.

Система проанализирует:
• Полноту ответа
• Понимание ключевых концепций  
• Наличие ошибок
• Даст персонализированные рекомендации

💡 *Пишите развернуто, как будто объясняете коллеге!*"""
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА ГЛАВНОГО МЕНЮ
            elif callback_text == "menu_main":
                text, keyboard = get_main_menu()
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА КУРСОВ
            elif callback_text.startswith("menu_course_"):
                course_name = callback_text.replace("menu_course_", "")
                text, keyboard = get_course_menu(course_name)
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА ПРЕМИУМ
            elif callback_text == "menu_premium":
                text, keyboard = get_premium_menu()
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА ПРОФИЛЯ
            elif callback_text == "menu_profile":
                text, keyboard = get_profile_menu(chat_id)
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА UBI
            elif callback_text == "menu_ubi":
                text, keyboard = get_ubi_menu()
                edit_main_message(chat_id, text, keyboard, message_id)
                return jsonify({"status": "ok"})
            
            # ОБРАБОТКА УРОКОВ
            elif callback_text.startswith('complete_'):
                lesson_hash = callback_text.replace('complete_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            update_user_progress(chat_id, lesson)
                            
                            # Возвращаем в меню курса после завершения урока
                            text, keyboard = get_course_menu(course_name)
                            success_text = f"✅ *Урок отмечен пройденным!*\n\n🎯 Получено: 10 баллов\n📚 Урок: {lesson}\n\n💫 Ваш прогресс растет!\n\n{text}"
                            
                            edit_main_message(chat_id, success_text, keyboard, message_id)
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('open_lesson_'):
                lesson_hash = callback_text.replace('open_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            # Генерируем AI-урок
                            ai_lesson = generate_ai_lesson(lesson, USER_PROGRESS.get(chat_id, {}).get('уровень', 1))
                            
                            # Создаем клавиатуру для урока
                            lesson_keyboard = {
                                "inline_keyboard": [
                                    [{"text": "✅ Завершить урок", "callback_data": f"complete_{lesson_hash}"}],
                                    [{"text": "🔙 Назад к курсу", "callback_data": f"menu_course_{course_name}"}]
                                ]
                            }
                            
                            lesson_text = f"📚 *{lesson}*\n\n{ai_lesson}"
                            edit_main_message(chat_id, lesson_text, lesson_keyboard, message_id)
                            break
                return jsonify({"status": "ok"})

        # Обработка обычных сообщений - ТОЛЬКО ДЛЯ ПЕРВОГО ЗАПУСКА
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if not chat_id:
            return jsonify({"status": "error", "message": "No chat_id"})

        # Если пользователь в режиме ответа на вопрос
        if chat_id in USER_CURRENT_TOPIC and text and not text.startswith('/'):
            topic = USER_CURRENT_TOPIC[chat_id]
            
            # Анализируем ответ с помощью AI-учителя
            evaluation = ai_teacher.evaluate_answer(text, topic)
            
            # Обновляем прогресс
            update_user_progress(chat_id, f"quiz_{topic}", evaluation["score"])
            
            # Формируем ответ
            progress = USER_PROGRESS.get(chat_id, {})
            stats = progress.get("статистика", {})
            success_rate = (stats.get("правильные_ответы", 0) / max(1, stats.get("всего_ответов", 0))) * 100
            
            response_text = f"""🎯 *РЕЗУЛЬТАТ ПРОВЕРКИ*

*Оценка:* {evaluation['score']}/5
*Сходство с эталоном:* {evaluation['similarity']:.2f}

{evaluation['feedback']}

---
📊 *Ваша статистика:*
• Уровень: {progress.get('уровень', 1)}
• Успеваемость: {success_rate:.1f}%
• Всего ответов: {stats.get('всего_ответов', 0)}

💫 *Продолжайте в том же духе!*"""
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🧠 Еще вопросы", "callback_data": f"quiz_{topic}"}],
                    [{"text": "🎓 Новые темы", "callback_data": "menu_learning"}],
                    [{"text": "🔙 Главное меню", "callback_data": "menu_main"}]
                ]
            }
            
            edit_main_message(chat_id, response_text, keyboard)
            # Сбрасываем текущую тему
            USER_CURRENT_TOPIC.pop(chat_id, None)
            return jsonify({"status": "ok"})

        # Обработка команды /start - СОЗДАЕМ ПЕРВОЕ СООБЩЕНИЕ
        if text == '/start':
            menu_text, menu_keyboard = get_main_menu()
            edit_main_message(chat_id, menu_text, menu_keyboard)
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

@app.route('/test-evaluation', methods=['POST'])
def test_evaluation():
    """Тестовый endpoint для проверки системы оценки"""
    data = request.json
    user_answer = data.get('answer', '')
    topic = data.get('topic', 'supervised_learning')
    
    evaluation = ai_teacher.evaluate_answer(user_answer, topic)
    
    return jsonify({
        "success": True,
        "evaluation": evaluation
    })

@app.route('/knowledge-topics', methods=['GET'])
def get_knowledge_topics():
    """Возвращает список доступных тем для обучения"""
    topics = {}
    for key, value in KNOWLEDGE_BASE.items():
        topics[key] = {
            "question": value["question"],
            "key_concepts": value["key_concepts"]
        }
    
    return jsonify({
        "success": True,
        "topics": topics
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)