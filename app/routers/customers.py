import models
from schemas import Customer, Customer_Response, Customer_Created, Customer_Delete
from utils import check_if_deleted
from database import get_db
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/", response_model = list[Customer_Response]) #get all customers
def get_all_customers(db: Session = Depends(get_db)):
    all_customers = db.query(models.Customers).filter(models.Customers.deleted_at == None).all()
    return all_customers


@router.get("/{id}", response_model = Customer_Response) #get single customer
def get_customer(id: int, db: Session = Depends(get_db)):
    selected_customer = db.query(models.Customers).filter(models.Customers.id == id, models.Customers.deleted_at == None).first()
    if not selected_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id {id} does not exist")
    return selected_customer


@router.post("/", response_model=Customer_Created) #create customer
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    new_customer = models.Customers(name = customer.name, email = customer.email, full_address = customer.full_address, phone_number = customer.phone_number)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@router.put("/{id}", response_model=Customer_Response) #update customer
def update_customer(id: int, updated_customer: Customer, db:Session = Depends(get_db)):
    query = db.query(models.Customers).filter(models.Customers.id == id, models.Customers.deleted_at == None)
    customer = query.first()
    if customer == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Customer with id {id} does not exist.")
    customer_data = updated_customer.model_dump()
    customer_data['updated_at'] = datetime.now()
    query.update(customer_data, synchronize_session=False)
    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/{id}")# delete customer
def soft_delete_customer(id: int, db:Session = Depends(get_db)):
    query = db.query(models.Customers).filter(models.Customers.id == id, models.Customers.deleted_at == None)
    customer = query.first()
    if customer == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Customer with id {id} does not exist.")
    query.update({"deleted_at": datetime.now()}, synchronize_session=False)
    db.commit()
    return "Customer has been deleted successfully"