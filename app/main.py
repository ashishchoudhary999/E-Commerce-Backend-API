from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .database import engine, Base
from . import models
from .routes import user, product, cart

app = FastAPI(title="E-Commerce API")

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(product.router)
app.include_router(cart.router)

@app.get("/")
def home():
    return {"message": "E-Commerce API is running"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="E-Commerce API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi