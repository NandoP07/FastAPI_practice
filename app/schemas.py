from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
   # id: int
    name: str
    description: str
    price: float
    stock: int
    # created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # deleted_at: Optional[str] = None

class Product_Delete(BaseModel):
    deleted_at: Optional[str] = None

class Customer(BaseModel):
    #id: int
    name: str
    email: str #BUSCAR TIPO EMAIL PARA VALIDACION DE DATOS
    full_address: Optional[str] = None
    phone_number: str
    # created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # deleted_at: Optional[str] = None

class Customer_Delete(BaseModel):
    deleted_at: Optional[str] = None