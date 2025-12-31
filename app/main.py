from fastapi import FastAPI
import models
from database import engine
from routers import customers, products, sales, seed
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(sales.router)
app.include_router(seed.router)