import threading
import time
from app import app
from bot import bot
from database import init_db

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def run_bot():
    print('Бот запущен')
    bot.infinity_polling()

if __name__ == '__main__':
    init_db()
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(2)
    run_bot()
