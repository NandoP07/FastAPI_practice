from schemas.product import Product_Update
import models
from schemas import Product, Product_Response, Product_Created, Product_Delete
from utils import check_if_deleted
from database import get_db
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_model = list[Product_Response])
def get_all_products(db: Session = Depends(get_db)):
    all_products = db.query(models.Products).filter(models.Products.deleted_at == None).all()
    return all_products

@router.get("/{id}", response_model = Product_Response) #get single product
def get_product(id: int, db: Session = Depends(get_db)):
  selected_product = db.query(models.Products).filter(models.Products.id == id, models.Products.deleted_at == None).first()
  if not selected_product:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist")
  return selected_product 

@router.post("/", response_model = Product_Created) #create products
def create_product(product: Product, db: Session = Depends(get_db)):
    new_product = models.Products(name = product.name, 
                                description = product.description, 
                                price = product.price, 
                                stock = product.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{id}", response_model = Product_Response) #update product
def update_product (id: int, updated_product: Product_Update, db:Session = Depends(get_db)):
    query = db.query(models.Products).filter(models.Products.id == id, models.Products.deleted_at == None)
    product = query.first()
    if product == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist.")
    product_data = updated_product.model_dump()
    product_data['updated_at'] = datetime.now()
    query.update(product_data, synchronize_session=False)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{id}")# delete product
def soft_delete_product(id: int, db:Session = Depends(get_db)):
    query = db.query(models.Products).filter(models.Products.id == id, models.Products.deleted_at == None)
    product = query.first()
    if product == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} does not exist.")
    query.update({"deleted_at": datetime.now()}, synchronize_session=False)
    db.commit()
    return "Product has been deleted successfully"

