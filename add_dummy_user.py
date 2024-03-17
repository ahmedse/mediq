# add_dummy_user.py

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User  # Adjust the import path according to your project structure

def create_dummy_user(db: Session, user_id: int):
    # Check if the user already exists to avoid duplicates
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is not None:
        print("User already exists!")
        return

    # Create a new dummy user instance
    dummy_user = User(id=user_id)
    db.add(dummy_user)
    db.commit()
    db.refresh(dummy_user)
    print(f"Added dummy user with ID: {dummy_user.id}")

def main():
    # Create a new database session
    db = SessionLocal()
    try:
        # Specify the dummy user's ID
        dummy_user_id = 2329987645
        create_dummy_user(db, dummy_user_id)
    finally:
        # Close the session
        db.close()

if __name__ == "__main__":
    main()