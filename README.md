# TaskControl Mini App

Telegram Mini App для управления задачами. Полностью на Python без JavaScript.

## Установка

```bash
pip install -r requirements.txt
```

Скачай ngrok: https://ngrok.com/download

## Запуск

### Способ 1: Автоматический (рекомендуется)

1. В первом терминале запусти ngrok:
```bash
ngrok http 5000
```

2. Во втором терминале запусти скрипт:
```bash
python start_with_ngrok.py
```

Скрипт автоматически получит HTTPS URL от ngrok и обновит конфигурацию.

### Способ 2: Ручной

1. В первом терминале запусти ngrok:
```bash
ngrok http 5000
```

2. Скопируй HTTPS URL (например: https://abc123.ngrok-free.app)

3. Открой `bot.py` и обнови `WEBAPP_URL`:
```python
WEBAPP_URL = 'https://abc123.ngrok-free.app'
```

4. Открой `app.py` и обнови `WEBAPP_URL`:
```python
WEBAPP_URL = 'https://abc123.ngrok-free.app'
```

5. Запусти приложение:
```bash
python main.py
```

## Использование

1. Открой бота в Telegram: @YourBotName
2. Нажми /start
3. Нажми кнопку "🚀 Открыть TaskControl"
4. Управляй задачами через Mini App

## Функции

- ✅ Создание задач с приоритетами и дедлайнами
- ✅ Редактирование задач
- ✅ Отметка задач как выполненных
- ✅ Удаление задач
- ✅ Фильтры: все, сегодня, неделя, просроченные, активные
- ✅ Уведомления в Telegram при всех действиях
- ✅ Адаптивный дизайн для всех устройств
- ✅ Премиум UI с glassmorphism эффектами

## Технологии

- Python + Flask (серверный рендеринг)
- Jinja2 (шаблоны)
- SQLAlchemy (база данных)
- pyTelegramBotAPI (Telegram бот)
- Без JavaScript
