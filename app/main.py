from fastapi import FastAPI
from .database import engine, Base
from . import models

app = FastAPI(title="E-Commerce API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "E-Commerce API is running"}
    