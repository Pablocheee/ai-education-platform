import httpx
from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests
import logging

app = Flask(__name__)

# Настройка API ключей
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), http_client=httpx.Client())
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# 🌌 БАЗА ЗНАНИЙ ОТ СИСТЕМЫ
COURSES = {
    "🚀 Войти в систему AI": {
        "уроки": [
            "🌌 Первый контакт: основы взаимодействия с AI",
            "⚡ Когнитивное ускорение: 10x продуктивности", 
        ],
        "уровень": "🎯 Инициация в новые возможности",
        "описание": "Освойте системы, которые определяют будущее."
    }
}

USER_PROGRESS = {}
USER_MESSAGE_IDS = {}
USER_LESSON_STATE = {}

# 🎯 УЛУЧШЕННЫЙ ДИАЛОГОВЫЙ AI-ПРЕПОДАВАТЕЛЬ
class DialogAITeacher:
    def generate_lesson_step(self, lesson_topic, user_level, conversation_history, current_step):
        """Генерирует следующий шаг урока"""
        
        system_prompt = f"""
        Ты - опытный AI-преподаватель NeuroTeacher. Будь кратким и конкретным.
        
        Тема урока: {lesson_topic}
        Уровень ученика: {user_level}/5
        
        История диалога:
        {self._format_conversation_history(conversation_history)}
        
        Правила:
        - Будь кратким (1-2 предложения)
        - Не повторяй предыдущие сообщения
        - Не говори "что ты чувствуешь?" 
        - Задавай конкретные вопросы
        - Если ученик прав - просто подтверди и иди дальше
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Продолжи урок кратко:"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content

    def _format_conversation_history(self, history):
        if not history:
            return "Начало урока"
        
        # Берем только последние 3 сообщения для контекста
        recent = history[-3:]
        return "\n".join([f"{'Ученик' if msg['role']=='student' else 'Учитель'}: {msg['content']}" for msg in recent])

# Инициализация преподавателя
dialog_teacher = DialogAITeacher()

def update_user_progress(chat_id, lesson_name):
    if chat_id not in USER_PROGRESS:
        USER_PROGRESS[chat_id] = {"пройденные_уроки": [], "уровень": 1, "баллы": 0}
    
    if lesson_name not in USER_PROGRESS[chat_id]["пройденные_уроки"]:
        USER_PROGRESS[chat_id]["пройденные_уроки"].append(lesson_name)

def update_lesson_state(chat_id, lesson_name, step=0, user_message=None):
    if chat_id not in USER_LESSON_STATE:
        USER_LESSON_STATE[chat_id] = {
            "current_lesson": lesson_name,
            "step": step,
            "conversation": []
        }
    
    if user_message:
        USER_LESSON_STATE[chat_id]["conversation"].append({
            "role": "student", 
            "content": user_message
        })

def add_teacher_response(chat_id, teacher_message):
    if chat_id in USER_LESSON_STATE:
        USER_LESSON_STATE[chat_id]["conversation"].append({
            "role": "teacher",
            "content": teacher_message
        })

# 🎯 УПРОЩЕННАЯ СИСТЕМА МЕНЮ
class MenuManager:
    def get_main_menu(self):
        keyboard = {
            "inline_keyboard": [
                [{"text": "🚀 Войти в систему AI", "callback_data": "menu_course_🚀 Войти в систему AI"}],
                [{"text": "👤 Мой профиль", "callback_data": "menu_profile"}]
            ]
        }
        
        text = """🧠 *NeuroTeacher*

Выбери курс:"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_course_menu(self, course_name, user_id):
        course_info = COURSES[course_name]
        
        lesson_buttons = []
        for i, lesson in enumerate(course_info['уроки']):
            lesson_buttons.append([
                {"text": f"📖 {lesson}", "callback_data": f"start_lesson_{hash(lesson)}"}
            ])
        
        lesson_buttons.append([{"text": "🔙 Назад", "callback_data": "menu_main"}])
        
        keyboard = {"inline_keyboard": lesson_buttons}
        
        text = f"""*{course_name}*

{course_info['описание']}

💫 *Выберите урок:*"""
        
        return {"text": text, "keyboard": keyboard}
    
    def get_dialog_lesson(self, chat_id, lesson_topic, user_input=None):
        user_level = USER_PROGRESS.get(chat_id, {}).get('уровень', 1)
        lesson_state = USER_LESSON_STATE.get(chat_id, {})
        
        conversation_history = lesson_state.get("conversation", [])
        current_step = lesson_state.get("step", 0)
        
        # Генерируем следующий шаг урока
        teacher_response = dialog_teacher.generate_lesson_step(
            lesson_topic, 
            user_level, 
            conversation_history, 
            current_step
        )
        
        # Добавляем ответ учителя в историю
        add_teacher_response(chat_id, teacher_response)
        
        # Обновляем шаг
        update_lesson_state(chat_id, lesson_topic, current_step + 1)
        
        # ПРОСТАЯ КЛАВИАТУРА
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ Завершить урок", "callback_data": f"complete_lesson_{hash(lesson_topic)}"}],
                [{"text": "🔙 Назад к курсу", "callback_data": "menu_course_back"}]
            ]
        }
        
        # ТОЛЬКО ТЕКУЩИЙ ОТВЕТ УЧИТЕЛЯ - БЕЗ ИСТОРИИ
        text = f"""📚 *{lesson_topic}*

{teacher_response}"""
        
        return {"text": text, "keyboard": keyboard}

# Инициализация менеджера
menu_manager = MenuManager()

def edit_main_message(chat_id, text, keyboard, message_id=None):
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

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
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
            
            if callback_text == "menu_main":
                menu_data = menu_manager.get_main_menu()
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith("menu_course_"):
                course_name = callback_text.replace("menu_course_", "")
                menu_data = menu_manager.get_course_menu(course_name, chat_id)
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('start_lesson_'):
                lesson_hash = callback_text.replace('start_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            # НАЧИНАЕМ С ЧИСТОГО СОСТОЯНИЯ
                            USER_LESSON_STATE[chat_id] = {
                                "current_lesson": lesson,
                                "step": 0,
                                "conversation": []
                            }
                            menu_data = menu_manager.get_dialog_lesson(chat_id, lesson)
                            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text.startswith('complete_lesson_'):
                lesson_hash = callback_text.replace('complete_lesson_', '')
                
                for course_name, course_info in COURSES.items():
                    for lesson in course_info['уроки']:
                        if hash(lesson) == int(lesson_hash):
                            update_user_progress(chat_id, lesson)
                            if chat_id in USER_LESSON_STATE:
                                del USER_LESSON_STATE[chat_id]
                            
                            menu_data = menu_manager.get_course_menu(course_name, chat_id)
                            success_text = f"✅ *Урок завершен!*\n\nВозвращаемся к курсу:\n\n{menu_data['text']}"
                            edit_main_message(chat_id, success_text, menu_data['keyboard'], message_id)
                            break
                return jsonify({"status": "ok"})
            
            elif callback_text == "menu_course_back":
                if chat_id in USER_LESSON_STATE:
                    del USER_LESSON_STATE[chat_id]
                menu_data = menu_manager.get_main_menu()
                edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], message_id)
                return jsonify({"status": "ok"})

        # ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if not chat_id:
            return jsonify({"status": "error", "message": "No chat_id"})

        if text == '/start':
            menu_data = menu_manager.get_main_menu()
            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'])
            return jsonify({"status": "ok"})
        
        lesson_state = USER_LESSON_STATE.get(chat_id, {})
        if lesson_state and "current_lesson" in lesson_state:
            current_lesson = lesson_state["current_lesson"]
            
            # ОТПРАВЛЯЕМ СООБЩЕНИЕ УЧЕНИКА ОТДЕЛЬНО
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"👤 *Вы:* {text}",
                    "parse_mode": "Markdown"
                }
            )
            
            # ОБНОВЛЯЕМ СОСТОЯНИЕ
            update_lesson_state(chat_id, current_lesson, lesson_state["step"], text)
            
            # ПОЛУЧАЕМ ОТВЕТ УЧИТЕЛЯ
            menu_data = menu_manager.get_dialog_lesson(chat_id, current_lesson, text)
            edit_main_message(chat_id, menu_data['text'], menu_data['keyboard'], USER_MESSAGE_IDS.get(chat_id))
            
            return jsonify({"status": "ok"})

        return jsonify({"status": "ok"})        
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)