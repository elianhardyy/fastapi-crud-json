# from fastapi import APIRouter
# from models.products import Products
# from config.database import collection_name
# from schema.products import list_serial
# from bson import ObjectId

# product_route = APIRouter()

# #GET REQUEST METHOD
# @product_route.get("/product")
# async def get_products():
#     products = list_serial(collection_name.find())
#     return products

# @product_route.post("/post")
# async def post_producst(products:Products):
#     collection_name.insert_one(dict(products))