import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.getenv("DB_PATH", os.path.join(PROJECT_ROOT, "ayurclinic.db"))
DATABASE_URL = f"sqlite:///{DB_PATH}"

print("DATABASE_URL in backend:", DATABASE_URL)
print("DB_PATH in backend:", DB_PATH)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()