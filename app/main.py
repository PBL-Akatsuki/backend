from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

try:
    from app import models, database, users, quizzes
except ImportError:
    import models
    import database
    import users
    import quizzes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["http://localhost:5173"]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Middleware for managing user sessions
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET", "super-secret-key"))

# Include Routers for Users and Quizzes
app.include_router(users.router)
app.include_router(quizzes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the NeoMyst Learning Platform!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
