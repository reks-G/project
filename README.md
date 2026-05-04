# TaskControl Mini App

Telegram Mini App для управления задачами. Полностью на Python без JavaScript.

## Структура проекта

```
TaskControl/
├── main.py              # Точка входа
├── app.py               # Flask приложение
├── bot.py               # Telegram бот
├── config.py            # Настройки
├── requirements.txt
├── database/
│   ├── models.py
│   ├── session.py
│   └── __init__.py
├── templates/           # HTML шаблоны (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── create.html
│   └── detail.html
└── static/
    └── style.css
```

## Установка

```bash
pip install -r requirements.txt
npm install -g localtunnel
```

## Настройка

Открой config.py и измени BOT_TOKEN

## Запуск

1. Запусти localtunnel:
```bash
lt --port 5000 --subdomain taskcontrol
```

2. Запусти приложение:
```bash
python main.py
```

## Особенности

- Серверный рендеринг на Python (Jinja2)
- Без JavaScript
- Модульная структура
- Flask + Telebot
