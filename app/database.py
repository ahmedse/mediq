# app\database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import AppConfig

# The AppConfig class would have attributes like DATABASE_URI that would be used here.
DATABASE_URI = AppConfig.DATABASE_URI

# Create the SQLAlchemy engine using the connection string from the config
engine = create_engine(DATABASE_URI, echo=AppConfig.SQLALCHEMY_ECHO)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()