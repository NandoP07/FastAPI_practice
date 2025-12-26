from fastapi import FastAPI
from app import models
from .database import engine
from .routers import customers, products
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(customers.router)
app.include_router(products.router)