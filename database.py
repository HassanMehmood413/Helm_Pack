import os
from sqlmodel import create_engine, SQLModel, Session

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres123@localhost:5432/proj2_db"
)

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)


# Function to create all tables
def create_db_and_tables():
    """Create all database tables defined in models"""
    SQLModel.metadata.create_all(engine)


# Dependency to get a database session
def get_db():
    with Session(engine) as session:
        yield session