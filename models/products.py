from pydantic import BaseModel

class Products(BaseModel):
    name:str
    description:str
    price:int
    qty:int