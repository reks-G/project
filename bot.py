from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import init_db

BOT_TOKEN = '8534316351:AAE-aCnUKL0jBNDlDV1jRaUjH_45Nhocggc'
WEBAPP_URL = 'https://taskcontrol-qu0a.onrender.com'

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')

def webapp_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('🚀 Открыть TaskControl', web_app=WebAppInfo(url=WEBAPP_URL)))
    return markup

def send_notification(telegram_id, message_text):
    """Отправить уведомление пользователю"""
    try:
        bot.send_message(telegram_id, message_text, reply_markup=webapp_button())
        return True
    except Exception as e:
        print(f'Ошибка отправки уведомления: {e}')
        return False

def notify_task_created(telegram_id, task_title):
    """Уведомление о создании задачи"""
    message = f'✅ <b>Задача создана</b>\n\n📝 {task_title}'
    return send_notification(telegram_id, message)

def notify_task_completed(telegram_id, task_title):
    """Уведомление о завершении задачи"""
    message = f'🎉 <b>Задача завершена!</b>\n\n✓ {task_title}'
    return send_notification(telegram_id, message)

def notify_task_deleted(telegram_id, task_title):
    """Уведомление об удалении задачи"""
    message = f'🗑 <b>Задача удалена</b>\n\n{task_title}'
    return send_notification(telegram_id, message)

def notify_task_updated(telegram_id, task_title):
    """Уведомление об обновлении задачи"""
    message = f'📝 <b>Задача обновлена</b>\n\n{task_title}'
    return send_notification(telegram_id, message)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}!\n\n'
        'Открой TaskControl Mini App для управления задачами:',
        reply_markup=webapp_button()
    )

if __name__ == '__main__':
    init_db()
    print('Бот запущен')
    bot.infinity_polling()
