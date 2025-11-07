from db import engine
from models import Base

# Створюємо всі таблиці у базі для перевірки
Base.metadata.create_all(engine)
