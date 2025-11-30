#-------------------
# Using SQLMODEL
#-------------------

from fastapi import FastAPI
from router import posts, users
from database import create_db_and_tables
from contextlib import asynccontextmanager
import models  # Import models so SQLModel knows about them


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")
    yield
    # Shutdown: cleanup if needed
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(posts.router)
app.include_router(users.router)



