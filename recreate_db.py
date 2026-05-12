"""
Пересоздание базы данных с правильной структурой
ВНИМАНИЕ: Это удалит все существующие данные!
"""
import os
from database import init_db

def recreate_database():
    db_file = 'taskcontrol.db'
    
    if os.path.exists(db_file):
        print(f"⚠️  Удаляем старую базу данных: {db_file}")
        os.remove(db_file)
        print("✅ Старая база удалена")
    
    print("📦 Создаем новую базу данных...")
    init_db()
    print("✅ База данных успешно создана с правильной структурой!")
    print("ℹ️  Все старые данные были удалены")

if __name__ == '__main__':
    response = input("⚠️  Это удалит все задачи! Продолжить? (yes/no): ")
    if response.lower() == 'yes':
        recreate_database()
    else:
        print("❌ Отменено")
