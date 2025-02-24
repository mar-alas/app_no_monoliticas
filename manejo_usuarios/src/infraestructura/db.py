from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infraestructura.models import Base

import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/user_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas si no existen
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
