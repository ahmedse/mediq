# db_init.py
import os
import sys
# Add the project root to the PYTHONPATH to allow for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.models import User
from app.database import engine, Base
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from config import AppConfig, logger

def create_initial_user(db_session):
    try:
        # Assuming 'id' is a required field and that User has attributes 'username' and 'email'
        user = User(
            id="2329987645",
            email="2329987645@example.com",
            # Include other fields and a hashed password for a real scenario
        )
        db_session.add(user)
        db_session.commit()
        logger.info("Initial user created.")
    except SQLAlchemyError as e:
        db_session.rollback()
        logger.error(f"Error creating initial user: {e}")
        raise

def init_db():
    try:
        # Log database info
        db_url = str(engine.url)
        db_name = db_url.split('/')[-1]  # Extract the database name
        logger.info(f"Initializing the database: {db_name}")

        # Create database tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables checked and created if not existing.")

        # Check if the initial user already exists
        with Session(engine) as db_session:
            user_count = db_session.query(User).count()
            if user_count == 0:
                # create_initial_user is a function you would define to add the initial user
                create_initial_user(db_session)
                logger.info("Initial user created.")
            else:
                logger.info("Initial user already exists. No new user created.")
    except Exception as e:
        logger.error(f"An error occurred while initializing the database: {e}")
        raise

if __name__ == '__main__':
    init_db()