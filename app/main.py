from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models as models
import app.database as database
import app.users as users

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
