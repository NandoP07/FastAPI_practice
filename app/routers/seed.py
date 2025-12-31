from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import random

router = APIRouter(
    prefix="/seed",
    tags=["Seed"]
)

@router.post("/")
def seed_database(db: Session = Depends(get_db)):
    # Create 10 Customers
    for i in range(1, 11):
        customer = models.Customers(
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
            full_address=f"Address {i}",
            phone_number=f"555-000{i}"
        )
        db.add(customer)

    # Create 10 Products
    for i in range(1, 11):
        product = models.Products(
            name=f"Product {i}",
            description=f"Description for Product {i}",
            price=float(random.randint(10, 100)),
            stock=random.randint(10, 50)
        )
        db.add(product)

    db.commit()
    return {"message": "Database seeded successfully with 10 customers and 10 products"}
