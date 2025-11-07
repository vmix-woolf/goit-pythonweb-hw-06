from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# Перевіряємо з’єднання
with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    print(result.fetchone())
