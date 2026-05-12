"""
Скрипт миграции базы данных - добавление колонки notified
"""
import sqlite3

def migrate():
    try:
        conn = sqlite3.connect('taskcontrol.db')
        cursor = conn.cursor()
        
        # Проверяем, существует ли колонка notified
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'notified' not in columns:
            print("➕ Добавляем колонку 'notified' в таблицу tasks...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN notified BOOLEAN DEFAULT 0")
            conn.commit()
            print("✅ Колонка 'notified' успешно добавлена!")
        else:
            print("ℹ️  Колонка 'notified' уже существует")
        
        conn.close()
        print("✅ Миграция завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка миграции: {e}")

if __name__ == '__main__':
    migrate()
