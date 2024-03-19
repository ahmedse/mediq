# conftest.py
import os
os.environ['ENVIRONMENT'] = 'testing'
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import engine, Base  # Adjust the import path according to your project structure
from app.db_init import init_db  # Import the init_db function, if you have one
from app.models import User  # Adjust the import path according to your project structure
from config import AppConfig, logger
