from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Default to localhost for local development
    "postgresql://user:password@localhost:5432/mydatabase"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

# Test database connection
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
except Exception as e:
    raise RuntimeError("Database connection test failed.") from e
