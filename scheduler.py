"""
Планировщик уведомлений для TaskControl
Отправляет уведомления за 30 минут до дедлайна
"""
import threading
import time
from datetime import datetime, timedelta
from database import get_session, Task, StatusEnum
from bot import bot

def check_upcoming_tasks():
    """Проверить задачи с приближающимся дедлайном"""
    while True:
        try:
            session = get_session()
            now = datetime.now()
            notification_time = now + timedelta(minutes=30)
            
            # Найти задачи с дедлайном через 25-35 минут (окно 10 минут)
            start_window = now + timedelta(minutes=25)
            end_window = now + timedelta(minutes=35)
            
            tasks = session.query(Task).filter(
                Task.due_at >= start_window,
                Task.due_at <= end_window,
                Task.status.in_([StatusEnum.pending, StatusEnum.in_progress]),
                Task.notified == False  # Еще не отправляли уведомление
            ).all()
            
            for task in tasks:
                try:
                    # Получить telegram_id пользователя
                    telegram_id = task.user.telegram_id
                    
                    # Отправить красивое уведомление
                    send_deadline_reminder(telegram_id, task)
                    
                    # Отметить что уведомление отправлено
                    task.notified = True
                    session.commit()
                    
                    print(f'✅ Отправлено напоминание для задачи: {task.title}')
                    
                except Exception as e:
                    print(f'❌ Ошибка отправки уведомления для задачи {task.id}: {e}')
            
            session.close()
            
        except Exception as e:
            print(f'❌ Ошибка проверки задач: {e}')
        
        # Проверять каждые 5 минут
        time.sleep(300)

def send_deadline_reminder(telegram_id, task):
    """Отправить красивое напоминание о дедлайне"""
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
    
    # Рассчитать оставшееся время
    time_left = task.due_at - datetime.now()
    minutes_left = int(time_left.total_seconds() / 60)
    
    # Определить эмодзи приоритета
    priority_emoji = {
        'low': '🟢',
        'medium': '🟡',
        'high': '🔴'
    }
    
    # Красивое сообщение
    message = f"""
⏰ <b>Напоминание о задаче</b>

{priority_emoji.get(task.priority.value, '⚪')} <b>{task.title}</b>

⏱ Осталось времени: <b>{minutes_left} минут</b>
📅 Дедлайн: {task.due_at.strftime('%d.%m.%Y в %H:%M')}

{'📝 ' + task.description[:100] + '...' if task.description and len(task.description) > 100 else '📝 ' + task.description if task.description else ''}

<i>Не забудьте выполнить задачу вовремя! 💪</i>
"""
    
    # Кнопка для открытия задачи
    markup = InlineKeyboardMarkup()
    
    # Импортируем WEBAPP_URL из bot.py
    from bot import WEBAPP_URL
    task_url = f"{WEBAPP_URL}/task/{task.id}?telegram_id={telegram_id}"
    
    markup.add(
        InlineKeyboardButton(
            '👁 Открыть задачу',
            web_app=WebAppInfo(url=task_url)
        )
    )
    markup.add(
        InlineKeyboardButton(
            '✅ Отметить выполненной',
            callback_data=f'complete_{task.id}'
        )
    )
    
    try:
        bot.send_message(
            telegram_id,
            message,
            parse_mode='HTML',
            reply_markup=markup
        )
    except Exception as e:
        print(f'Ошибка отправки сообщения: {e}')

def start_scheduler():
    """Запустить планировщик в фоновом потоке"""
    scheduler_thread = threading.Thread(target=check_upcoming_tasks, daemon=True)
    scheduler_thread.start()
    print('📅 Планировщик уведомлений запущен')
