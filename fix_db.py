import sqlite3
import sys

try:
    conn = sqlite3.connect('taskcontrol.db')
    cursor = conn.cursor()
    
    # Проверяем колонки
    cursor.execute('PRAGMA table_info(tasks)')
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'notified' in columns:
        print('Колонка notified уже существует')
    else:
        print('Добавляем колонку notified...')
        cursor.execute('ALTER TABLE tasks ADD COLUMN notified BOOLEAN DEFAULT 0')
        conn.commit()
        print('Колонка notified успешно добавлена!')
    
    conn.close()
    sys.exit(0)
    
except Exception as e:
    print(f'Ошибка: {e}')
    sys.exit(1)
