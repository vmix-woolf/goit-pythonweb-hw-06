import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool
from alembic import context

# Імпортуємо базовий клас з моделей
from models import Base

# Завантажуємо змінні з .env
load_dotenv()

# Конфіг Alembic
config = context.config
DATABASE_URL = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск у офлайн-режимі (без підключення до БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск у онлайн-режимі (з підключенням до БД)."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

