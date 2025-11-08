import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# ---- 1. Завантажуємо .env ----
load_dotenv()

# ---- 2. Імпортуємо базовий клас ----
from models import Base

# ---- 3. Конфіг Alembic ----
config = context.config

# ---- 4. Читаємо URL з .env ----
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL не знайдено в .env")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ---- 5. Налаштовуємо логування Alembic ----
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск у офлайн-режимі (без підключення до БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск у онлайн-режимі (з підключенням до БД)."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
