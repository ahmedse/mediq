# app/db_init.py
from .database import engine, Base
from . import models

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()