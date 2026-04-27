import threading
from flask import Flask, request, jsonify, send_from_directory
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import get_session, User, Task, PriorityEnum, StatusEnum, init_db
from datetime import datetime, timedelta
import hmac
import hashlib

BOT_TOKEN = '8534316351:AAE-aCnUKL0jBNDlDV1jRaUjH_45Nhocggc'
DATABASE_URL = 'sqlite:///taskcontrol.db'
WEBAPP_URL = 'https://taskcontrol.loca.lt'

app = Flask(__name__, static_folder='mini_app', static_url_path='')
bot = TeleBot(BOT_TOKEN, parse_mode='HTML')

@app.route('/')
def index():
    return send_from_directory('mini_app', 'index.html')

@app.route('/api/user', methods=['POST'])
def get_or_create_user():
    data = request.json
    telegram_id = data.get('telegram_id')
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=data.get('username'),
            first_name=data.get('first_name')
        )
        session.add(user)
        session.commit()
    
    result = {'id': user.id, 'telegram_id': user.telegram_id}
    session.close()
    return jsonify(result)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    telegram_id = request.args.get('telegram_id')
    filter_type = request.args.get('filter', 'all')
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    
    if not user:
        session.close()
        return jsonify([])
    
    query = session.query(Task).filter_by(user_id=user.id)
    
    if filter_type == 'today':
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        query = query.filter(Task.due_at >= today_start, Task.due_at < today_end)
    elif filter_type == 'week':
        week_start = datetime.now()
        week_end = week_start + timedelta(days=7)
        query = query.filter(Task.due_at >= week_start, Task.due_at < week_end)
    elif filter_type == 'overdue':
        query = query.filter(Task.due_at < datetime.now(), Task.status == StatusEnum.pending)
    elif filter_type == 'active':
        query = query.filter(Task.status.in_([StatusEnum.pending, StatusEnum.in_progress]))
    
    tasks = query.order_by(Task.due_at).all()
    
    result = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat() if task.created_at else None,
        'due_at': task.due_at.isoformat() if task.due_at else None,
        'priority': task.priority.value,
        'status': task.status.value
    } for task in tasks]
    
    session.close()
    return jsonify(result)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    telegram_id = data.get('telegram_id')
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    
    if not user:
        session.close()
        return jsonify({'error': 'User not found'}), 404
    
    task = Task(
        user_id=user.id,
        title=data.get('title'),
        description=data.get('description'),
        due_at=datetime.fromisoformat(data.get('due_at')) if data.get('due_at') else None,
        priority=PriorityEnum[data.get('priority', 'medium')]
    )
    
    session.add(task)
    session.commit()
    
    result = {'id': task.id, 'message': 'Task created'}
    session.close()
    return jsonify(result)

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    telegram_id = data.get('telegram_id')
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    task = session.query(Task).filter_by(id=task_id, user_id=user.id).first()
    
    if not task:
        session.close()
        return jsonify({'error': 'Task not found'}), 404
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'due_at' in data:
        task.due_at = datetime.fromisoformat(data['due_at']) if data['due_at'] else None
    if 'priority' in data:
        task.priority = PriorityEnum[data['priority']]
    if 'status' in data:
        task.status = StatusEnum[data['status']]
    
    session.commit()
    session.close()
    return jsonify({'message': 'Task updated'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    telegram_id = request.args.get('telegram_id')
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    task = session.query(Task).filter_by(id=task_id, user_id=user.id).first()
    
    if task:
        session.delete(task)
        session.commit()
    
    session.close()
    return jsonify({'message': 'Task deleted'})

def webapp_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('🚀 Открыть TaskControl', web_app=WebAppInfo(url=WEBAPP_URL)))
    return markup

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}!\n\n'
        'Открой TaskControl Mini App для управления задачами:',
        reply_markup=webapp_button()
    )

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def run_bot():
    print('Бот запущен!')
    bot.infinity_polling()

if __name__ == '__main__':
    print('Инициализация базы данных...')
    init_db()
    
    print('Запуск Flask сервера...')
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    import time
    time.sleep(2)
    
    run_bot()
