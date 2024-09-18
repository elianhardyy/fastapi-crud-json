from pydantic import BaseModel
from config.database import Base
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,increment=True)
    product_name=Column(String(255))
    description=Column(String(255))
    price=Column(Integer)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)