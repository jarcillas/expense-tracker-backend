# scripts/database_init.py (or database_init.py)
from sqlalchemy import create_engine
from expense_tracker_backend.models import Base  # Replace with your actual import path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_engine(DATABASE_URL)


def create_tables():
    """
    Create all database tables defined in SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()
