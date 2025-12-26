from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Customer(BaseModel):
    #id: int
    name: str
    email: str #BUSCAR TIPO EMAIL PARA VALIDACION DE DATOS
    full_address: Optional[str] = None
    phone_number: str
    # created_at: Optional[str] = None
    updated_at: Optional[datetime] = None
    # deleted_at: Optional[str] = None

class Customer_Created(BaseModel):
    id: int
    name: str
    email: str #BUSCAR TIPO EMAIL PARA VALIDACION DE DATOS
    full_address: str
    phone_number: str
    created_at: datetime

class Customer_Response(BaseModel):
    name: str
    email: str
    full_address: Optional[str] = None
    phone_number: str
    
    class Config:
        orm_mode = True

class Customer_Delete(BaseModel):
    deleted_at: Optional[datetime] = None
