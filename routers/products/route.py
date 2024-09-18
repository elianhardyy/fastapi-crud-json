from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from models.products import Products
from config.database import collection_name, SessionLocal
from schema.products import list_serial
from models.products import Products
# from bson import ObjectId

product_route = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# #GET REQUEST METHOD
# @product_route.get("/product")
# async def get_products():
#     products = list_serial(collection_name.find())
#     return products

# @product_route.post("/post")
# async def post_producst(products:Products):
#     collection_name.insert_one(dict(products))

@product_route.post("/add/product",status_code=status.HTTP_201_CREATED)
async def create_product(products:Products, db:Session=Depends(get_db)):
    db_products = Products(**products.dict())
    db.add(db_products)
    db.commit()
    db.refresh(db_products)
    return db_products