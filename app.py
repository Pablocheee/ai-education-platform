from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging
import time
from datetime import datetime, timedelta
import json
import random

app = Flask(__name__)

# Настройка API ключей
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TON_WALLET = os.getenv('TON_WALLET', 'UQAVTMHfwYcMn7ttJNXiJVaoA-jjRTeJHc2sjpkAVzc84oSY')

# 🧠 УМНАЯ СИСТЕМА ОБУЧЕНИЯ
class SmartLearningSystem:
    def __init__(self):
        self.user_profiles = {}
        self.learning_analytics = {}
    
    def analyze_learning_style(self, user_id, interaction_data):
        """Анализирует стиль обучения пользователя"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "learning_style": "balanced",
                "preferred_times": [],
                "attention_span": 15,
                "completion_rate": 0,
                "engagement_level": 1
            }
        
        # Анализ данных взаимодействия
        profile = self.user_profiles[user_id]
        
        # Определяем стиль обучения на основе поведения
        if interaction_data.get("completion_time", 0) < 300:  # Быстро завершает
            profile["learning_style"] = "fast_paced"
        elif interaction_data.get("reviews", 0) > 3:  # Много повторений
            profile["learning_style"] = "thorough"
        
        return profile
    
    def get_personalized_recommendations(self, user_id):
        """Персонализированные рекомендации обучения"""
        profile = self.user_profiles.get(user_id, {})
        
        recommendations = {
            "fast_paced": "🎯 Рекомендуем микро-уроки по 5-7 минут",
            "thorough": "📚 Лучше подойдут глубокие погружения по 20-30 минут", 
            "balanced": "⚖️ Оптимальны стандартные уроки по 15 минут"
        }
        
        return recommendations.get(profile.get("learning_style", "balanced"), 
                                "🎯 Начните со стандартных уроков")

class EnergySystem:
    """Система энергии и фокуса"""
    
    def __init__(self):
        self.user_energy = {}
        self.max_energy = 100
    
    def get_user_energy(self, user_id):
        """Возвращает текущий уровень энергии пользователя"""
        if user_id not in self.user_energy:
            self.user_energy[user_id] = {
                "current": self.max_energy,
                "last_update": datetime.now(),
                "daily_usage": 0
            }
        
        energy_data = self.user_energy[user_id]
        
        # Восстановление энергии со временем (1 энергия в 10 минут)
        time_diff = datetime.now() - energy_data["last_update"]
        energy_gain = min(int(time_diff.total_seconds() / 600), self.max_energy)
        
        if energy_gain > 0:
            energy_data["current"] = min(energy_data["current"] + energy_gain, self.max_energy)
            energy_data["last_update"] = datetime.now()
        
        return energy_data
    
    def use_energy(self, user_id, amount=10):
        """Использует энергию для урока"""
        energy_data = self.get_user_energy(user_id)
        
        if energy_data["current"] >= amount:
            energy_data["current"] -= amount
            energy_data["daily_usage"] += amount
            return True
        return False
    
    def get_energy_status(self, user_id):
        """Возвращает статус энергии для отображения"""
        energy_data = self.get_user_energy(user_id)
        energy_percent = (energy_data["current"] / self.max_energy) * 100
        
        if energy_percent >= 70:
            emoji = "⚡"
        elif energy_percent >= 30:
            emoji = "🔋" 
        else:
            emoji = "🪫"
        
        return f"{emoji} Энергия: {energy_data['current']}/{self.max_energy}"

class FormatSelector:
    """Умный выбор формата обучения"""
    
    def __init__(self):
        self.formats = {
            "micro": {
                "duration": "5-7 минут",
                "energy_cost": 10,
                "focus_required": "низкий",
                "best_for": ["утро", "перерыв", "мобильные"]
            },
            "standard": {
                "duration": "15-20 минут", 
                "energy_cost": 25,
                "focus_required": "средний",
                "best_for": ["вечер", "дома", "пк"]
            },
            "deep_dive": {
                "duration": "30-45 минут",
                "energy_cost": 50,
                "focus_required": "высокий", 
                "best_for": ["выходные", "погружение"]
            }
        }
    
    def select_optimal_format(self, user_id, context=None):
        """Выбирает оптимальный формат обучения"""
        current_hour = datetime.now().hour
        energy_system = EnergySystem()
        user_energy = energy_system.get_user_energy(user_id)["current"]
        
        # Анализ контекста
        if context is None:
            context = {}
        
        # Утренние часы (6-10) - микро-формат
        if 6 <= current_hour <= 10:
            preferred_format = "micro"
        # Обеденное время (12-14) - микро-формат  
        elif 12 <= current_hour <= 14:
            preferred_format = "micro"
        # Вечерние часы (18-22) - стандарт или глубокое погружение
        elif 18 <= current_hour <= 22:
            if user_energy >= 40:
                preferred_format = "deep_dive"
            else:
                preferred_format = "standard"
        # Ночные часы - не рекомендуется учиться
        elif 23 <= current_hour or current_hour <= 5:
            preferred_format = "micro"  # Короткие уроки если нужно
        else:
            preferred_format = "standard"
        
        # Корректировка на основе энергии
        format_energy = self.formats[preferred_format]["energy_cost"]
        if user_energy < format_energy:
            # Ищем формат с меньшим потреблением энергии
            for format_name, format_info in self.formats.items():
                if format_info["energy_cost"] <= user_energy:
                    preferred_format = format_name
                    break
        
        return preferred_format

class InteractiveMicroLessons:
    """Система интерактивных микро-уроков"""
    
    def __init__(self):
        self.lesson_templates = {
            "problem_solution": """
🎯 *Проблема:* {problem}
💡 *Решение:* {solution}
🚀 *Действие:* {action}

*Практическое задание:*
{exercise}

⏱️ Время выполнения: 3-5 минут
            """,
            "concept_application": """
📚 *Концепция:* {concept}
🔧 *Применение:* {application} 
💫 *Результат:* {result}

*Попробуйте прямо сейчас:*
{try_now}

✅ Проверка: {check}
            """,
            "quick_win": """
⚡ *Быстрая победа:* {win}
🎯 *Фокус на:* {focus}
🚀 *Следующий шаг:* {next_step}

*Мини-упражнение:*
{mini_exercise}
            """
        }
    
    def generate_micro_lesson(self, topic, format_type="micro"):
        """Генерирует интерактивный микро-урок"""
        
        prompts = {
            "micro": f"""
            Создай МИКРО-урок (5-7 минут) на тему: "{topic}"
            
            Структура:
            1. 🎯 ОДНА ключевая идея (самое важное)
            2. 💡 Практическое применение (3 конкретных шага)
            3. 🚀 Быстрый результат (что получит прямо сейчас)
            4. ⚡ Интерактивное упражнение (2-3 минуты)
            
            Требования:
            - Максимально практично
            - Можно применить сразу
            - Интерактивный элемент
            """,
            "interactive": f"""
            Создай ИНТЕРАКТИВНЫЙ урок на тему: "{topic}"
            
            Включи:
            - 🤔 Вопрос для размышления
            - 🛠️ Практическое задание с шагами
            - ✅ Мгновенную самопроверку
            - 📈 Прогресс-трекер
            
            Формат: диалоговый, вовлекающий
            """
        }
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты создаешь интерактивные микро-уроки. Делай их практичными, вовлекающими и с мгновенной обратной связью."},
                    {"role": "user", "content": prompts.get(format_type, prompts["micro"])}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            lesson = response.choices[0].message.content
            
            # Добавляем интерактивные элементы
            interactive_elements = self._add_interactive_elements(topic)
            return lesson + "\n\n" + interactive_elements
            
        except Exception as e:
            return f"📚 *{topic}*\n\nБазовый урок. AI система временно недоступна."

    def _add_interactive_elements(self, topic):
        """Добавляет интерактивные элементы к уроку"""
        elements = [
            f"🎯 *Быстрая самопроверка:*\n💡 Ответьте на вопрос по теме '{topic}'",
            f"⚡ *Мгновенное применение:*\nПопробуйте применить знания в течение 2 минут", 
            f"📊 *Ваш прогресс:*\n✅ Понимание концепции: █████░░░░ 60%"
        ]
        return random.choice(elements)

class ProgressTracker:
    """Система отслеживания прогресса в реальном времени"""
    
    def __init__(self):
        self.lesson_progress = {}
    
    def start_lesson(self, user_id, lesson_name):
        """Начинает отслеживание прогресса урока"""
        if user_id not in self.lesson_progress:
            self.lesson_progress[user_id] = {}
        
        self.lesson_progress[user_id][lesson_name] = {
            "start_time": datetime.now(),
            "checkpoints": [],
            "completion_percent": 0,
            "current_section": 0,
            "total_sections": 5  # Стандартное количество секций
        }
    
    def update_progress(self, user_id, lesson_name, section_completed):
        """Обновляет прогресс прохождения урока"""
        if user_id in self.lesson_progress and lesson_name in self.lesson_progress[user_id]:
            progress = self.lesson_progress[user_id][lesson_name]
            progress["current_section"] = section_completed
            progress["completion_percent"] = int((section_completed / progress["total_sections"]) * 100)
            progress["checkpoints"].append({
                "section": section_completed,
                "timestamp": datetime.now()
            })
    
    def get_progress_bar(self, user_id, lesson_name):
        """Возвращает строку прогресс-бара"""
        if user_id in self.lesson_progress and lesson_name in self.lesson_progress[user_id]:
            percent = self.lesson_progress[user_id][lesson_name]["completion_percent"]
            bars = int(percent / 10)
            return f"📊 Прогресс: {'█' * bars}{'░' * (10 - bars)} {percent}%"
        return "📊 Прогресс: ░░░░░░░░░░ 0%"

class LearningPsychologist:
    """AI-психолог обучения"""
    
    def __init__(self):
        self.user_mood = {}
        self.burnout_risk = {}
    
    def analyze_engagement(self, user_id, learning_data):
        """Анализирует вовлеченность и риск выгорания"""
        if user_id not in self.user_mood:
            self.user_mood[user_id] = {
                "engagement_score": 50,
                "fatigue_level": 0,
                "motivation_trend": "stable",
                "last_break": datetime.now()
            }
        
        profile = self.user_mood[user_id]
        
        # Анализ риска выгорания
        time_since_break = datetime.now() - profile["last_break"]
        if time_since_break.total_seconds() > 7200:  # 2 часа
            profile["fatigue_level"] += 10
            profile["engagement_score"] -= 5
        
        # Рекомендации на основе анализа
        recommendations = []
        if profile["fatigue_level"] > 60:
            recommendations.append("💡 Рекомендуем сделать перерыв 15-20 минут")
        if profile["engagement_score"] < 30:
            recommendations.append("🎯 Попробуйте сменить тему или формат обучения")
        
        return {
            "mood_profile": profile,
            "recommendations": recommendations,
            "burnout_risk": "высокий" if profile["fatigue_level"] > 70 else "средний" if profile["fatigue_level"] > 40 else "низкий"
        }
    
    def get_optimal_learning_time(self, user_id):
        """Рекомендует оптимальное время для обучения"""
        # Простой алгоритм на основе времени суток
        current_hour = datetime.now().hour
        
        if 9 <= current_hour <= 11:
            return "🌅 Утренние часы - отличное время для обучения!"
        elif 16 <= current_hour <= 18:
            return "🌇 Дневное время - хорошая продуктивность"
        elif 20 <= current_hour <= 22:
            return "🌙 Вечернее время - подходит для закрепления"
        else:
            return "💡 Любое время хорошо для обучения!"

# Инициализация всех систем
smart_learning = SmartLearningSystem()
energy_system = EnergySystem() 
format_selector = FormatSelector()
micro_lessons = InteractiveMicroLessons()
progress_tracker = ProgressTracker()
learning_psychologist = LearningPsychologist()

# 📊 БАЗА ДАННЫХ И АНАЛИТИКА
class LearningAnalytics:
    """Система аналитики обучения"""
    
    def __init__(self):
        self.learning_data = {}
    
    def track_learning_session(self, user_id, lesson_data):
        """Отслеживает сессию обучения"""
        session_id = f"{user_id}_{datetime.now().timestamp()}"
        
        self.learning_data[session_id] = {
            "user_id": user_id,
            "lesson": lesson_data.get("lesson_name"),
            "start_time": datetime.now(),
            "duration": 0,
            "completion_rate": 0,
            "engagement_metrics": {},
            "format_used": lesson_data.get("format"),
            "energy_used": lesson_data.get("energy_used", 0)
        }
    
    def get_user_insights(self, user_id):
        """Возвращает инсайты по пользователю"""
        user_sessions = [s for s in self.learning_data.values() if s["user_id"] == user_id]
        
        if not user_sessions:
            return {"message": "Недостаточно данных для анализа"}
        
        total_sessions = len(user_sessions)
        avg_duration = sum(s["duration"] for s in user_sessions) / total_sessions
        completion_rate = sum(s["completion_rate"] for s in user_sessions) / total_sessions
        
        # Анализ предпочтений
        preferred_format = max(
            set(s["format_used"] for s in user_sessions),
            key=list(s["format_used"] for s in user_sessions).count
        )
        
        return {
            "total_sessions": total_sessions,
            "average_duration": f"{avg_duration:.1f} мин",
            "completion_rate": f"{completion_rate:.1f}%",
            "preferred_format": preferred_format,
            "learning_consistency": "высокая" if total_sessions > 5 else "средняя" if total_sessions > 2 else "низкая"
        }

# 🎮 РАСШИРЕННАЯ СИСТЕМА ГЕЙМИФИКАЦИИ
class AdvancedGamification:
    """Продвинутая система геймификации"""
    
    def __init__(self):
        self.achievements = {
            "streak_3": {"name": "🔥 Серия из 3 дней", "points": 30},
            "streak_7": {"name": "🎯 Серия из 7 дней", "points": 70},
            "fast_learner": {"name": "⚡ Быстрый ученик", "points": 25},
            "knowledge_explorer": {"name": "🌍 Исследователь знаний", "points": 40},
            "energy_master": {"name": "⚡ Мастер энергии", "points": 35}
        }
        
        self.leaderboard = {}
    
    def update_streak(self, user_id):
        """Обновляет серию дней обучения"""
        today = datetime.now().date().isoformat()
        
        if user_id not in self.leaderboard:
            self.leaderboard[user_id] = {
                "current_streak": 1,
                "longest_streak": 1,
                "last_learning_date": today,
                "total_points": 0
            }
        
        user_data = self.leaderboard[user_id]
        last_date = datetime.fromisoformat(user_data["last_learning_date"]).date()
        current_date = datetime.now().date()
        
        if (current_date - last_date).days == 1:
            user_data["current_streak"] += 1
            user_data["longest_streak"] = max(user_data["longest_streak"], user_data["current_streak"])
        elif (current_date - last_date).days > 1:
            user_data["current_streak"] = 1
        
        user_data["last_learning_date"] = today
        
        # Проверка достижений серии
        new_achievements = []
        if user_data["current_streak"] == 3:
            new_achievements.append(self.achievements["streak_3"])
        elif user_data["current_streak"] == 7:
            new_achievements.append(self.achievements["streak_7"])
        
        return new_achievements
    
    def get_leaderboard(self, top_n=10):
        """Возвращает таблицу лидеров"""
        sorted_users = sorted(
            self.leaderboard.items(),
            key=lambda x: x[1]["total_points"],
            reverse=True
        )[:top_n]
        
        leaderboard_text = "🏆 *ТОП-10 УЧЕНИКОВ*\n\n"
        for i, (user_id, data) in enumerate(sorted_users, 1):
            leaderboard_text += f"{i}. 🎯 {data['total_points']} очков (серия: {data['current_streak']} дн.)\n"
        
        return leaderboard_text

# Инициализация дополнительных систем
learning_analytics = LearningAnalytics()
advanced_gamification = AdvancedGamification()

# 🎯 ИНТЕГРАЦИЯ В СУЩЕСТВУЮЩИЙ КОД

# ДОБАВИТЬ в обработку уроков:
def generate_adaptive_lesson_with_systems(lesson_topic, user_id):
    """Генерирует адаптивный урок со всеми системами"""
    
    # 1. Выбор оптимального формата
    optimal_format = format_selector.select_optimal_format(user_id)
    
    # 2. Проверка энергии
    energy_status = energy_system.get_energy_status(user_id)
    if not energy_system.use_energy(user_id, 10):
        return f"🪫 *Недостаточно энергии!*\n\n{energy_status}\n\nПодождите восстановления энергии или сделайте перерыв."
    
    # 3. Генерация урока
    lesson_content = micro_lessons.generate_micro_lesson(lesson_topic, optimal_format)
    
    # 4. Начало отслеживания прогресса
    progress_tracker.start_lesson(user_id, lesson_topic)
    
    # 5. Анализ психолога
    psychologist_advice = learning_psychologist.get_optimal_learning_time(user_id)
    
    # 6. Обновление серии
    streak_achievements = advanced_gamification.update_streak(user_id)
    
    # Сборка финального сообщения
    final_lesson = f"""
{lesson_content}

---
{energy_status}
{progress_tracker.get_progress_bar(user_id, lesson_topic)}
💡 {psychologist_advice}
    """
    
    # Уведомление о достижениях
    if streak_achievements:
        achievements_text = "\n".join([f"🎉 {ach['name']} (+{ach['points']} очков)" for ach in streak_achievements])
        final_lesson += f"\n\n{achievements_text}"
    
    return final_lesson

# 📱 КОНТЕКСТНО-АВТОНОМНОЕ ОБУЧЕНИЕ
class ContextAwareLearning:
    """Учет контекста для автономного обучения"""
    
    def get_contextual_recommendations(self, user_id):
        """Рекомендации на основе контекста"""
        current_time = datetime.now()
        hour = current_time.hour
        weekday = current_time.weekday()
        
        # Рекомендации по времени суток
        if hour < 12:
            time_recommendation = "🌅 Утро - лучшее время для новых тем"
        elif hour < 18:
            time_recommendation = "🌇 День - подходит для практики"
        else:
            time_recommendation = "🌙 Вечер - время для закрепления"
        
        # Рекомендации по дням недели
        if weekday < 5:
            day_recommendation = "📅 Будний день - короткие сессии эффективны"
        else:
            day_recommendation = "🎉 Выходной - можно погрузиться глубже"
        
        return f"{time_recommendation}\n{day_recommendation}"

# Инициализация контекстной системы
context_learning = ContextAwareLearning()

# 🎨 МУЛЬТИ-МОДАЛЬНОЕ ОБУЧЕНИЕ
class MultiModalLearning:
    """Поддержка разных форматов контента"""
    
    def generate_learning_content(self, topic, content_type="text"):
        """Генерирует контент разных типов"""
        
        prompts = {
            "text": f"Создай текстовый урок на тему: {topic}",
            "audio": f"Создай сценарий для аудио-урока на тему: {topic}",
            "visual": f"Опиши визуальные материалы для темы: {topic}",
            "interactive": f"Создай сценарий интерактивного упражнения для: {topic}"
        }
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Ты создаешь образовательный контент разных форматов."},
                    {"role": "user", "content": prompts.get(content_type, prompts["text"])}
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Контент для {topic} временно недоступен."

# 🔧 ИНТЕГРАЦИЯ С СУЩЕСТВУЮЩИМ КОДОМ

# В обработчике callback_query ДОБАВИТЬ:
elif callback_text.startswith('open_lesson_'):
    lesson_hash = callback_text.replace('open_lesson_', '')
    
    for course_name, course_info in COURSES.items():
        for lesson in course_info['уроки']:
            if str(hash(lesson)) == lesson_hash:
                # ИСПОЛЬЗУЕМ НОВУЮ СИСТЕМУ
                ai_lesson = generate_adaptive_lesson_with_systems(lesson, chat_id)
                
                inline_keyboard = {
                    "inline_keyboard": [[
                        {"text": "✅ Завершить урок", "callback_data": f"complete_{lesson_hash}"},
                        {"text": "📊 Прогресс", "callback_data": "show_progress"}
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

# ДОБАВИТЬ новые команды в обработчик сообщений:
elif text == "📊 Моя аналитика":
    insights = learning_analytics.get_user_insights(chat_id)
    response_text = f"""📊 *ВАША АНАЛИТИКА ОБУЧЕНИЯ*

🎯 Сессий: {insights['total_sessions']}
⏱️ Средняя длительность: {insights['average_duration']}
✅ Завершаемость: {insights['completion_rate']}
📚 Предпочтительный формат: {insights['preferred_format']}
📈 Постоянство: {insights['learning_consistency']}"""

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": response_text,
            "parse_mode": "Markdown"
        }
    )

elif text == "🏆 Лидерборд":
    leaderboard_text = advanced_gamification.get_leaderboard()
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
        json={
            "chat_id": chat_id,
            "text": leaderboard_text,
            "parse_mode": "Markdown"
        }
    )

elif text == "💡 Рекомендации":
    recommendations = context_learning.get_contextual_recommendations(chat_id)
    psych_advice = learning_psychologist.get_optimal_learning_time(chat_id)
    
    response_text = f"""💡 *ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ*

{recommendations}
{psych_advice}

{energy_system.get_energy_status(chat_id)}"""

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id, 
            "text": response_text,
            "parse_mode": "Markdown"
        }
    )

# ОБНОВИТЬ главное меню:
keyboard = {
    "keyboard": [
        ["🚀 Войти в систему AI", "💫 Запустить эволюцию"],
        ["🌌 База знаний", "⚡ Карьерный ускоритель"],
        ["💰 Премиум доступ", "👤 Мой профиль"],
        ["📊 Моя аналитика", "🏆 Лидерборд", "💡 Рекомендации"],
        ["👛 Мой UBI кошелек", "🌍 UBI Система"]
    ],
    "resize_keyboard": True
}