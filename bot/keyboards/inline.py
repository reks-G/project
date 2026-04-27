from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import WEBAPP_URL

def webapp_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('🚀 Открыть TaskControl', web_app=WebAppInfo(url=WEBAPP_URL)))
    return markup
