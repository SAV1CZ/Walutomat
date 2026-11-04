from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from urllib.parse import quote_plus         
from dotenv import load_dotenv                                                                                                  
import os

load_dotenv()
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@localhost:5432/walutomat_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()