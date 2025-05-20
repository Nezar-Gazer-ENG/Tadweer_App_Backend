import sys
import os

# Dynamically add the project root to the PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, '../..'))
sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from app.utils.config_loader import get_config
from app.models.base import Base  # Use the unified Base

# Retrieve database credentials from environment variables
DB_USER = get_config("DB_USER", "root")
DB_PASSWORD = get_config("DB_PASSWORD", "Nezar*18102003")
DB_HOST = get_config("DB_HOST", "localhost")
DB_PORT = get_config("DB_PORT", "3306")
DB_NAME = get_config("DB_NAME", "tire_app")

# Database URL for SQLAlchemy
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=True
)

# Create a scoped session for database interactions
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test the database connection
def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Database connection successful.")
            result = connection.execute(text("SELECT DATABASE();"))
            db_name = result.fetchone()[0]
            print(f"Connected to database: {db_name}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

# Run the test on import
if __name__ == "__main__":
    test_connection()
