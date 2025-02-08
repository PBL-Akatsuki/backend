from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import os

try:
    from app import models, database, users, quizzes, seed
except ImportError:
    import models
    import database
    import users
    import quizzes
    import seed

# Create all tables
models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed the database
    print("Seeding the database...")
    seed.seed_data()  # Calls your seeding function
    yield
    # Shutdown: add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
