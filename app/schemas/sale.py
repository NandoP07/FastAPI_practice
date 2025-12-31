from pydantic import BaseModel
from typing import List
from datetime import datetime

# Represents a single item in the shopping cart (input)
class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

# Represents the sale creation request (input)
class SaleCreate(BaseModel):
    customer_id: int
    items: List[SaleItemCreate]

# Represents a single item in the sale response (output)
class SaleDetailResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    
    class Config:
        orm_mode = True

# Represents the sale response (output)
class SaleResponse(BaseModel):
    id: int
    customer_id: int
    date: datetime
    total: float
    items: List[SaleDetailResponse] = [] # Note: This might need adjustement in the router to populate correctly from the relationship

    class Config:
        orm_mode = True
