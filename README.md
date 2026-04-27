# TaskControl Mini App

Telegram Mini App для управления задачами.

## Установка

```bash
pip install -r requirements.txt
npm install -g localtunnel
```

## Настройка

Открой main.py и измени:
- `BOT_TOKEN` - токен от @BotFather
- `WEBAPP_URL` - URL от localtunnel (по умолчанию https://taskcontrol.loca.lt)

## Запуск

1. В одном терминале запусти localtunnel:
```bash
lt --port 5000 --subdomain taskcontrol
```

2. В другом терминале запусти приложение:
```bash
python main.py
```

Всё! Flask и бот запустятся автоматически.

## Функции

- Создание задач
- Фильтрация задач
- Просмотр деталей
- Отметка выполненных
- Удаление задач
