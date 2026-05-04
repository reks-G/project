from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from database import init_db

BOT_TOKEN = '8534316351:AAE-aCnUKL0jBNDlDV1jRaUjH_45Nhocggc'
WEBAPP_URL = 'https://taskcontrol.loca.lt'

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')

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

if __name__ == '__main__':
    init_db()
    print('Бот запущен')
    bot.infinity_polling()
