from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Product(BaseModel):
   # id: int
    name: str
    description: str
    price: float
    stock: int
    # created_at: Optional[str] = None
    # updated_at: Optional[datetime] = None
    # deleted_at: Optional[str] = None

class Product_Response(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    
    class Config:
        orm_mode = True

class Product_Update(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class Product_Created(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class Product_Delete(BaseModel):
    deleted_at: Optional[datetime] = None
