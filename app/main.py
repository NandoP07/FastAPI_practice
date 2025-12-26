from sqlalchemy.sql._elements_constructors import null
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from app import models
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models import Customer, Product
from .schemas import Product, Customer, Product_Delete, Customer_Delete, Product_Update, Product_Response, Customer_Response, Customer_Created, Product_Created
from .utils import check_if_deleted
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#---------------------------------Experimental---------------------------------------------------------------------------

#---------------------------------Experimental---------------------------------------------------------------------------


@app.get("/products", response_model = list[Product_Response])
def get_all_products(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).filter(models.Product.deleted_at == None).all()
    return all_products

@app.get("/products/{id}", response_model = Product_Response) #get single product
def get_product(id: int, db: Session = Depends(get_db)):
  selected_product = db.query(models.Product).filter(models.Product.id == id).first()
  if not selected_product:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist")
  check_if_deleted(selected_product)
  return selected_product 


@app.get("/customers", response_model = list[Customer_Response]) #get all customers
def get_all_customers(db: Session = Depends(get_db)):
    all_customers = db.query(models.Customer).filter(models.Customer.deleted_at == None).all()
    return all_customers

@app.get("/customers/{id}", response_model = Customer_Response) #get single customer
def get_customer(id: int, db: Session = Depends(get_db)):
    selected_customer = db.query(models.Customer).filter(models.Customer.id == id, models.Customer.deleted_at == None).first()
    if not selected_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id {id} does not exist")
    return selected_customer

@app.post("/products", response_model = Product_Created) #create products
def create_product(product: Product, db: Session = Depends(get_db)):
    new_product = models.Product(name = product.name, description = product.description, price = product.price, stock = product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



    
@app.post("/customers", response_model=Customer_Created) #create customer
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    new_customer = models.Customer(name = customer.name, email = customer.email, full_address = customer.full_address, phone_number = customer.phone_number)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@app.put("/products/{id}") #update product
def update_product (id: int, updated_product: Product_Update, db:Session = Depends(get_db)):
    query = db.query(models.Product).filter(models.Product.id == id)
    product = query.first()
    if product == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist.")
    product_data = updated_product.dict()
    product_data['updated_at'] = datetime.now()
    query.update(product_data, synchronize_session=False)
    db.commit()
    return "Product has been updated successfully"

@app.put("/customers/{id}") #update customer
def update_customer(id: int, updated_customer: Customer, db:Session = Depends(get_db)):
    query = db.query(models.Customer).filter(models.Customer.id == id)
    customer = query.first()
    if customer == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Customer with id {id} does not exist.")
    customer_data = updated_customer.dict()
    customer_data['updated_at'] = datetime.now()
    query.update(customer_data, synchronize_session=False)
    db.commit()
    return "Customer has been updated successfully"

@app.delete("/products/{id}")# delete product
def soft_delete_product(id: int, delete_product: Product_Delete, db:Session = Depends(get_db)):
    query = db.query(models.Product).filter(models.Product.id == id)
    product = query.first()
    if product == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist.")
    check_if_deleted(product)
    product_data = delete_product.dict()
    product_data['deleted_at'] = datetime.now()
    query.update(product_data, synchronize_session=False)
    db.commit()
    return "Product has been deleted successfully"

@app.delete("/customers/{id}")# delete customer
def soft_delete_customer(id: int, delete_customer: Customer_Delete, db:Session = Depends(get_db)):
    query = db.query(models.Customer).filter(models.Customer.id == id)
    customer = query.first()
    if customer == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Customer with id {id} does not exist.")
    check_if_deleted(customer)
    customer_data = delete_customer.dict()
    customer_data['deleted_at'] = datetime.now()
    query.update(customer_data, synchronize_session=False)
    db.commit()
    return "Customer has been deleted successfully"