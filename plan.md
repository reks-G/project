Что: Telegram-таскменеджер для создания и отслеживания задач с дедлайнами и приоритетами.

Кому: фрилансеры, команды, студенты — любой пользователь Telegram.

Ключевой сценарий: создать задачу (заголовок, ТЗ, дедлайн, приоритет) → бот напомнит → пользователь отмечает выполненной.

MVP:

CRUD задач (title, description, due_at, priority, status).
Напоминания (24ч, 1ч, при дедлайне).
Фильтрация: сегодня, неделя, просроченные, по приоритету.
Аутентификация по Telegram user_id.
Технологии:

Python, Telebot (pyTelegramBotAPI), Telegram Web Apps (опционально).
SQLAlchemy + PostgreSQL (или SQLite).
APScheduler для напоминаний.
Alembic, pydantic.
Структура данных (основное):

users (telegram_id, username, settings)
tasks (id, user_id, title, description, created_at, due_at, priority, status)
Команды/кнопки:

/start

Доп. фичи:

Проекты/теги, повторяющиеся задачи, совместная работа, импорт/экспорт, статистика.