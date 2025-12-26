from app.schemas.product import Product_Update
from .. import models
from ..schemas import Product, Product_Response, Product_Created, Product_Delete
from ..utils import check_if_deleted
from ..database import get_db
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()

@router.get("/products", response_model = list[Product_Response])
def get_all_products(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).filter(models.Product.deleted_at == None).all()
    return all_products

@router.get("/products/{id}", response_model = Product_Response) #get single product
def get_product(id: int, db: Session = Depends(get_db)):
  selected_product = db.query(models.Product).filter(models.Product.id == id).first()
  if not selected_product:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist")
  check_if_deleted(selected_product)
  return selected_product 

@router.post("/products", response_model = Product_Created) #create products
def create_product(product: Product, db: Session = Depends(get_db)):
    new_product = models.Product(name = product.name, description = product.description, price = product.price, stock = product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/products/{id}") #update product
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

@router.delete("/products/{id}")# delete product
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

