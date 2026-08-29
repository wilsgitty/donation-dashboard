import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from pathlib import Path

load_dotenv()

DB_USER = os.getenv("MYSQLUSER") or os.getenv("DB_USER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD") or os.getenv("MYSQL_ROOT_PASSWORD") or os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("MYSQLHOST") or os.getenv("DB_HOST")
DB_PORT = os.getenv("MYSQLPORT") or os.getenv("DB_PORT")
DB_NAME = os.getenv("MYSQLDATABASE") or os.getenv("MYSQL_DATABASE") or os.getenv("DB_NAME")

from urllib.parse import quote_plus

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()