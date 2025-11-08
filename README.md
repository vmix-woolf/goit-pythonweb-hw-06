## University Database CLI

Простий CLI-інтерфейс для керування університетською базою даних через SQLAlchemy і argparse.

### Вимоги
- Python 3.12+
- Poetry
- PostgreSQL (контейнер university-postgres або локальна база)

Таблиці створюються через Alembic:
```
poetry run alembic upgrade head
```

### Запуск проєкту

- Активуйте середовище Poetry:

```poetry shell```

- Перевірте підключення до бази (.env повинен містити параметр):

```DATABASE_URL=postgresql+psycopg2://postgres:sl_pass@localhost:5433/university_db```

### Використання CLI

CLI підтримує базові CRUD-операції для моделей:
Student, Teacher, Group, Subject, Grade

#### Приклади:

##### Створення викладача:
```poetry run python main.py -a create -m Teacher -n "Борис Джонсон"```

##### Список викладачів:
```poetry run python main.py -a list -m Teacher```

##### Оновлення імені викладача:
```poetry run python main.py -a update -m Teacher --id 1 -n "Андрій Безос"```

##### Видалення викладача:
```poetry run python main.py -a remove -m Teacher --id 1```

### Структура проєкту
- models.py — SQLAlchemy моделі
- db.py — налаштування бази даних і сесії
- main.py — CLI для CRUD-операцій
- alembic/ — міграції бази
- .env — параметри підключення (DATABASE_URL)