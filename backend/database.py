import entities
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def CreateDB():

    entities.Base.metadata.create_all(bind=engine)
    print("Database created")


# Dependency to get DB session
def Get_db() -> Session:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    CreateDB()