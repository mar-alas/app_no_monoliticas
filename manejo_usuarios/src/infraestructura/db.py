import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infraestructura.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@user_db/user_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
