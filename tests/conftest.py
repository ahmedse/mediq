# conftest.py
import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine, SessionLocal
from app.db_init import init_db  # Import the init_db function
from app.models import User  # Adjust the import path according to your project structure

# Add the project root directory to the sys.path
sys.path.append(str(Path(__file__).parent.parent))
# conftest.py
# Define the test database URL
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

# Create a test engine instance
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a test session local
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module")
def test_db():
    # Create the tables in the test database
    Base.metadata.create_all(bind=test_engine)
    # Create a new session for the test
    db_session = TestSessionLocal()
    try:
        yield db_session  # Use the session in tests
    finally:
        # Close the session after the tests are done
        db_session.close()
        # Drop the tables after the tests are done
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="module")
def dummy_user(test_db):
    # Use the provided test database session to add a dummy user
    user = User(id="2329987645")  # Set the registration number as the ID
    test_db.add(user)
    test_db.commit()

    yield user  # This user can now be used in tests

    # Clean up: delete the dummy user after the tests that use this fixture are done
    test_db.delete(user)
    test_db.commit()