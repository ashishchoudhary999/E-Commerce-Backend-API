from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import user

app = FastAPI(title="E-Commerce API")

Base.metadata.create_all(bind=engine)

app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "E-Commerce API is running"}
    