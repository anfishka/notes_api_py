from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к SQL Server
DATABASE_URL = "mssql+pyodbc://@localhost/notes_db?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

# Настройка движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# Сессии для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Зависимость для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()